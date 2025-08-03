"""
Cliente HTTP para a API da ALEPE.
"""
import asyncio
import logging
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin, urlencode

import httpx
from httpx import HTTPStatusError, RequestError, TimeoutException

from src.config import settings
from src.validators import APIRequest, build_query_params


logger = logging.getLogger(__name__)


class ALEPEHTTPClient:
    """Cliente HTTP para a API da ALEPE."""
    
    def __init__(self) -> None:
        """Inicializa o cliente HTTP."""
        self._client: Optional[httpx.AsyncClient] = None
        self._rate_limiter = RateLimiter(settings.rate_limit_requests)
    
    async def __aenter__(self) -> "ALEPEHTTPClient":
        """Entrada do context manager."""
        await self.start()
        return self
    
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Saída do context manager."""
        await self.close()
    
    async def start(self) -> None:
        """Inicializa o cliente HTTP."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(settings.timeout),
                headers={
                    "User-Agent": settings.user_agent,
                    "Accept": "application/json, text/csv, */*",
                    "Accept-Encoding": "gzip, deflate",
                },
                follow_redirects=True,
            )
        logger.info("Cliente HTTP inicializado")
    
    async def close(self) -> None:
        """Fecha o cliente HTTP."""
        if self._client:
            await self._client.aclose()
            self._client = None
        logger.info("Cliente HTTP fechado")
    
    def _build_url(self, endpoint: str, params: Dict[str, str]) -> str:
        """
        Constrói a URL completa para a requisição.
        
        Args:
            endpoint: Nome do endpoint
            params: Parâmetros de query
            
        Returns:
            URL completa
        """
        base_url = f"{settings.alepe_base_url}/{endpoint}"
        if params:
            query_string = urlencode(params)
            return f"{base_url}?{query_string}"
        return base_url
    
    async def _make_request(
        self,
        url: str,
        method: str = "GET",
        **kwargs: Any
    ) -> httpx.Response:
        """
        Faz uma requisição HTTP com retry e rate limiting.
        
        Args:
            url: URL da requisição
            method: Método HTTP
            **kwargs: Argumentos adicionais para a requisição
            
        Returns:
            Resposta HTTP
            
        Raises:
            HTTPStatusError: Se a resposta tem status de erro
            RequestError: Se houve erro na requisição
            TimeoutException: Se a requisição excedeu o timeout
        """
        if not self._client:
            await self.start()
        
        # Aplicar rate limiting
        await self._rate_limiter.acquire()
        
        last_exception = None
        
        for attempt in range(settings.max_retries):
            try:
                logger.debug(f"Tentativa {attempt + 1} para {method} {url}")
                
                response = await self._client.request(method, url, **kwargs)
                response.raise_for_status()
                
                logger.debug(f"Requisição bem-sucedida: {response.status_code}")
                return response
                
            except (HTTPStatusError, RequestError, TimeoutException) as e:
                last_exception = e
                logger.warning(
                    f"Tentativa {attempt + 1} falhou para {url}: {str(e)}"
                )
                
                if attempt < settings.max_retries - 1:
                    delay = settings.retry_delay * (2 ** attempt)  # Exponential backoff
                    logger.debug(f"Aguardando {delay}s antes da próxima tentativa")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Todas as tentativas falharam para {url}")
        
        # Se chegou aqui, todas as tentativas falharam
        raise last_exception
    
    async def fetch_data(self, request: APIRequest) -> Union[Dict[str, Any], List[Dict[str, Any]], str]:
        """
        Busca dados da API da ALEPE.
        
        Args:
            request: Objeto da requisição validada
            
        Returns:
            Dados da API (JSON ou CSV como string)
            
        Raises:
            ValueError: Se os dados não podem ser processados
            HTTPStatusError: Se a API retorna erro
        """
        # Constrói os parâmetros de query
        params = build_query_params(request)
        
        # Constrói a URL
        url = self._build_url(request.endpoint, params)
        logger.info(f"Buscando dados de: {url}")
        
        try:
            # Faz a requisição
            response = await self._make_request(url)
            
            # Processa a resposta baseado no formato
            if request.formato == "json":
                try:
                    data = response.json()
                    logger.info(f"Dados JSON recebidos: {len(data) if isinstance(data, list) else 'objeto'} item(s)")
                    return data
                except ValueError as e:
                    logger.error(f"Erro ao decodificar JSON: {e}")
                    raise ValueError(f"Resposta não é um JSON válido: {e}")
            
            elif request.formato == "csv":
                data = response.text
                logger.info(f"Dados CSV recebidos: {len(data.splitlines())} linha(s)")
                return data
            
            else:
                raise ValueError(f"Formato não suportado: {request.formato}")
        
        except HTTPStatusError as e:
            logger.error(f"Erro HTTP {e.response.status_code}: {e.response.text}")
            raise ValueError(
                f"Erro na API da ALEPE (HTTP {e.response.status_code}): "
                f"{e.response.text[:200]}..."
            )
        
        except RequestError as e:
            logger.error(f"Erro de requisição: {e}")
            raise ValueError(f"Erro de conexão com a API da ALEPE: {str(e)}")
        
        except TimeoutException as e:
            logger.error(f"Timeout na requisição: {e}")
            raise ValueError("Timeout na requisição à API da ALEPE")
    
    async def get_available_endpoints(self) -> Dict[str, str]:
        """
        Retorna os endpoints disponíveis na API.
        
        Returns:
            Dicionário com endpoints e suas descrições
        """
        return settings.available_endpoints.copy()
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Verifica se a API está funcionando.
        
        Returns:
            Dicionário com o status da API
        """
        try:
            # Tenta buscar dados básicos de parlamentares
            from validators import ParlamentarRequest
            
            request = ParlamentarRequest(formato="json")
            
            # Faz uma requisição simples
            start_time = asyncio.get_event_loop().time()
            await self.fetch_data(request)
            end_time = asyncio.get_event_loop().time()
            
            response_time = end_time - start_time
            
            return {
                "status": "healthy",
                "api_url": settings.alepe_base_url,
                "response_time_seconds": round(response_time, 3),
                "available_endpoints": list(settings.available_endpoints.keys())
            }
        
        except Exception as e:
            logger.error(f"Health check falhou: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "api_url": settings.alepe_base_url
            }


class RateLimiter:
    """Rate limiter simples baseado em token bucket."""
    
    def __init__(self, requests_per_minute: int) -> None:
        """
        Inicializa o rate limiter.
        
        Args:
            requests_per_minute: Número máximo de requisições por minuto
        """
        self.requests_per_minute = requests_per_minute
        self.tokens = requests_per_minute
        self.last_update = asyncio.get_event_loop().time()
        self._lock = asyncio.Lock()
    
    async def acquire(self) -> None:
        """Adquire um token para fazer uma requisição."""
        async with self._lock:
            now = asyncio.get_event_loop().time()
            
            # Adiciona tokens baseado no tempo decorrido
            elapsed = now - self.last_update
            self.tokens = min(
                self.requests_per_minute,
                self.tokens + elapsed * (self.requests_per_minute / 60.0)
            )
            self.last_update = now
            
            # Se não há tokens disponíveis, espera
            if self.tokens < 1:
                sleep_time = (1 - self.tokens) / (self.requests_per_minute / 60.0)
                logger.debug(f"Rate limit atingido, aguardando {sleep_time:.2f}s")
                await asyncio.sleep(sleep_time)
                self.tokens = 0
            else:
                self.tokens -= 1


# Instância global do cliente (será inicializada quando necessário)
_client_instance: Optional[ALEPEHTTPClient] = None


async def get_client() -> ALEPEHTTPClient:
    """
    Retorna uma instância do cliente HTTP.
    
    Returns:
        Instância do cliente HTTP
    """
    global _client_instance
    
    if _client_instance is None:
        _client_instance = ALEPEHTTPClient()
        await _client_instance.start()
    
    return _client_instance


async def close_client() -> None:
    """Fecha o cliente HTTP global."""
    global _client_instance
    
    if _client_instance:
        await _client_instance.close()
        _client_instance = None
"""
Ferramentas MCP para a API da ALEPE.
"""
import logging
from typing import Any, Dict, List, Optional, Union

from fastmcp import FastMCP
from pydantic import BaseModel, Field

from src.config import settings, ENDPOINT_FILTERS
from src.http_client import get_client
from src.validators import validate_request_parameters


logger = logging.getLogger(__name__)


class EndpointInfo(BaseModel):
    """Informações sobre um endpoint da API."""
    name: str = Field(..., description="Nome do endpoint")
    description: str = Field(..., description="Descrição do endpoint")
    available_filters: List[str] = Field(..., description="Filtros disponíveis")


class APIResponse(BaseModel):
    """Resposta da API formatada."""
    success: bool = Field(..., description="Se a requisição foi bem-sucedida")
    data: Optional[Union[Dict[str, Any], List[Dict[str, Any]], str]] = Field(None, description="Dados retornados")
    error: Optional[str] = Field(None, description="Mensagem de erro, se houver")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadados da resposta")


def register_alepe_tools(mcp: FastMCP) -> None:
    """Registra todas as ferramentas da ALEPE no servidor MCP."""
    
    @mcp.tool()
    async def list_available_endpoints() -> List[EndpointInfo]:
        """
        Lista todos os endpoints disponíveis na API da ALEPE.
        
        Returns:
            Lista de endpoints com suas descrições e filtros disponíveis.
        """
        try:
            endpoints = []
            
            for endpoint_name, description in settings.available_endpoints.items():
                available_filters = ENDPOINT_FILTERS.get(endpoint_name, [])
                
                endpoints.append(EndpointInfo(
                    name=endpoint_name,
                    description=description,
                    available_filters=available_filters
                ))
            
            logger.info(f"Listando {len(endpoints)} endpoints disponíveis")
            return endpoints
        
        except Exception as e:
            logger.error(f"Erro ao listar endpoints: {e}")
            raise

    @mcp.tool()
    async def get_parlamentares(
        formato: str = "json",
        partido: Optional[str] = None,
        situacao: Optional[str] = None,
        legislatura: Optional[int] = None
    ) -> APIResponse:
        """
        Busca dados dos deputados estaduais da ALEPE.
        
        Args:
            formato: Formato dos dados (json ou csv)
            partido: Sigla do partido (ex: PT, PSDB)
            situacao: Situação do parlamentar (ativo ou inativo)
            legislatura: Número da legislatura
        
        Returns:
            Dados dos parlamentares.
        """
        try:
            params = {
                "formato": formato,
                "partido": partido,
                "situacao": situacao,
                "legislatura": legislatura
            }
            params = {k: v for k, v in params.items() if v is not None}
            
            request = validate_request_parameters("parlamentares", params)
            
            client = await get_client()
            data = await client.fetch_data(request)
            
            metadata = {
                "endpoint": "parlamentares",
                "formato": formato,
                "filtros_aplicados": {k: v for k, v in params.items() if k != "formato" and v is not None}
            }
            
            if isinstance(data, list):
                metadata["total_registros"] = len(data)
            elif isinstance(data, str) and formato == "csv":
                metadata["total_linhas"] = len(data.splitlines())
            
            logger.info(f"Dados de parlamentares obtidos com sucesso")
            
            return APIResponse(
                success=True,
                data=data,
                metadata=metadata
            )
        
        except Exception as e:
            logger.error(f"Erro ao buscar parlamentares: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                metadata={"endpoint": "parlamentares"}
            )

    @mcp.tool()
    async def get_servidores(
        formato: str = "json",
        vinculo: Optional[str] = None,
        situacao: Optional[str] = None,
        cargo: Optional[str] = None,
        lotacao: Optional[str] = None
    ) -> APIResponse:
        """
        Busca dados dos servidores da ALEPE.
        
        Args:
            formato: Formato dos dados (json ou csv)
            vinculo: Tipo de vínculo (efetivo, comissionado, terceirizado, estagiario)
            situacao: Situação do servidor (ativo ou inativo)
            cargo: Cargo do servidor
            lotacao: Lotação do servidor
        
        Returns:
            Dados dos servidores.
        """
        try:
            params = {
                "formato": formato,
                "vinculo": vinculo,
                "situacao": situacao,
                "cargo": cargo,
                "lotacao": lotacao
            }
            params = {k: v for k, v in params.items() if v is not None}
            
            request = validate_request_parameters("servidores", params)
            
            client = await get_client()
            data = await client.fetch_data(request)
            
            metadata = {
                "endpoint": "servidores",
                "formato": formato,
                "filtros_aplicados": {k: v for k, v in params.items() if k != "formato" and v is not None}
            }
            
            if isinstance(data, list):
                metadata["total_registros"] = len(data)
            elif isinstance(data, str) and formato == "csv":
                metadata["total_linhas"] = len(data.splitlines())
            
            logger.info(f"Dados de servidores obtidos com sucesso")
            
            return APIResponse(
                success=True,
                data=data,
                metadata=metadata
            )
        
        except Exception as e:
            logger.error(f"Erro ao buscar servidores: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                metadata={"endpoint": "servidores"}
            )

    @mcp.tool()
    async def get_contratos(
        formato: str = "json",
        ano: Optional[int] = None,
        valor_min: Optional[float] = None,
        valor_max: Optional[float] = None,
        fornecedor: Optional[str] = None
    ) -> APIResponse:
        """
        Busca dados dos contratos da ALEPE.
        
        Args:
            formato: Formato dos dados (json ou csv)
            ano: Ano do contrato
            valor_min: Valor mínimo do contrato
            valor_max: Valor máximo do contrato
            fornecedor: Nome ou CNPJ do fornecedor
        
        Returns:
            Dados dos contratos.
        """
        try:
            params = {
                "formato": formato,
                "ano": ano,
                "valor_min": valor_min,
                "valor_max": valor_max,
                "fornecedor": fornecedor
            }
            params = {k: v for k, v in params.items() if v is not None}
            
            request = validate_request_parameters("contratos", params)
            
            client = await get_client()
            data = await client.fetch_data(request)
            
            metadata = {
                "endpoint": "contratos",
                "formato": formato,
                "filtros_aplicados": {k: v for k, v in params.items() if k != "formato" and v is not None}
            }
            
            if isinstance(data, list):
                metadata["total_registros"] = len(data)
            elif isinstance(data, str) and formato == "csv":
                metadata["total_linhas"] = len(data.splitlines())
            
            logger.info(f"Dados de contratos obtidos com sucesso")
            
            return APIResponse(
                success=True,
                data=data,
                metadata=metadata
            )
        
        except Exception as e:
            logger.error(f"Erro ao buscar contratos: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                metadata={"endpoint": "contratos"}
            )

    @mcp.tool()
    async def get_licitacoes(
        formato: str = "json",
        ano: Optional[int] = None,
        modalidade: Optional[str] = None,
        situacao: Optional[str] = None
    ) -> APIResponse:
        """
        Busca dados das licitações da ALEPE.
        
        Args:
            formato: Formato dos dados (json ou csv)
            ano: Ano da licitação
            modalidade: Modalidade da licitação
            situacao: Situação da licitação
        
        Returns:
            Dados das licitações.
        """
        try:
            params = {
                "formato": formato,
                "ano": ano,
                "modalidade": modalidade,
                "situacao": situacao
            }
            params = {k: v for k, v in params.items() if v is not None}
            
            request = validate_request_parameters("licitacoes", params)
            
            client = await get_client()
            data = await client.fetch_data(request)
            
            metadata = {
                "endpoint": "licitacoes",
                "formato": formato,
                "filtros_aplicados": {k: v for k, v in params.items() if k != "formato" and v is not None}
            }
            
            if isinstance(data, list):
                metadata["total_registros"] = len(data)
            elif isinstance(data, str) and formato == "csv":
                metadata["total_linhas"] = len(data.splitlines())
            
            logger.info(f"Dados de licitações obtidos com sucesso")
            
            return APIResponse(
                success=True,
                data=data,
                metadata=metadata
            )
        
        except Exception as e:
            logger.error(f"Erro ao buscar licitações: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                metadata={"endpoint": "licitacoes"}
            )

    @mcp.tool()
    async def get_remuneracao(
        formato: str = "json",
        ano: Optional[int] = None,
        mes: Optional[int] = None,
        vinculo: Optional[str] = None
    ) -> APIResponse:
        """
        Busca dados de remuneração da ALEPE.
        
        Args:
            formato: Formato dos dados (json ou csv)
            ano: Ano da remuneração
            mes: Mês da remuneração (1-12)
            vinculo: Tipo de vínculo (efetivo, comissionado, terceirizado)
        
        Returns:
            Dados de remuneração.
        """
        try:
            params = {
                "formato": formato,
                "ano": ano,
                "mes": mes,
                "vinculo": vinculo
            }
            params = {k: v for k, v in params.items() if v is not None}
            
            request = validate_request_parameters("remuneracao", params)
            
            client = await get_client()
            data = await client.fetch_data(request)
            
            metadata = {
                "endpoint": "remuneracao",
                "formato": formato,
                "filtros_aplicados": {k: v for k, v in params.items() if k != "formato" and v is not None}
            }
            
            if isinstance(data, list):
                metadata["total_registros"] = len(data)
            elif isinstance(data, str) and formato == "csv":
                metadata["total_linhas"] = len(data.splitlines())
            
            logger.info(f"Dados de remuneração obtidos com sucesso")
            
            return APIResponse(
                success=True,
                data=data,
                metadata=metadata
            )
        
        except Exception as e:
            logger.error(f"Erro ao buscar remuneração: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                metadata={"endpoint": "remuneracao"}
            )

    @mcp.tool()
    async def get_cargos(formato: str = "json") -> APIResponse:
        """
        Busca dados dos cargos disponíveis na ALEPE.
        
        Args:
            formato: Formato dos dados (json ou csv)
        
        Returns:
            Dados dos cargos.
        """
        try:
            params = {"formato": formato}
            
            request = validate_request_parameters("cargos", params)
            
            client = await get_client()
            data = await client.fetch_data(request)
            
            metadata = {
                "endpoint": "cargos",
                "formato": formato
            }
            
            if isinstance(data, list):
                metadata["total_registros"] = len(data)
            elif isinstance(data, str) and formato == "csv":
                metadata["total_linhas"] = len(data.splitlines())
            
            logger.info(f"Dados de cargos obtidos com sucesso")
            
            return APIResponse(
                success=True,
                data=data,
                metadata=metadata
            )
        
        except Exception as e:
            logger.error(f"Erro ao buscar cargos: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                metadata={"endpoint": "cargos"}
            )

    @mcp.tool()
    async def get_lotacoes(formato: str = "json") -> APIResponse:
        """
        Busca dados das lotações organizacionais da ALEPE.
        
        Args:
            formato: Formato dos dados (json ou csv)
        
        Returns:
            Dados das lotações.
        """
        try:
            params = {"formato": formato}
            
            request = validate_request_parameters("lotacoes", params)
            
            client = await get_client()
            data = await client.fetch_data(request)
            
            metadata = {
                "endpoint": "lotacoes",
                "formato": formato
            }
            
            if isinstance(data, list):
                metadata["total_registros"] = len(data)
            elif isinstance(data, str) and formato == "csv":
                metadata["total_linhas"] = len(data.splitlines())
            
            logger.info(f"Dados de lotações obtidos com sucesso")
            
            return APIResponse(
                success=True,
                data=data,
                metadata=metadata
            )
        
        except Exception as e:
            logger.error(f"Erro ao buscar lotações: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                metadata={"endpoint": "lotacoes"}
            )

    @mcp.tool()
    async def search_data(
        endpoint: str,
        formato: str = "json",
        filters: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """
        Busca dados de qualquer endpoint da ALEPE com filtros personalizados.
        
        Args:
            endpoint: Nome do endpoint (parlamentares, servidores, contratos, etc.)
            formato: Formato dos dados (json ou csv)
            filters: Dicionário com filtros específicos para o endpoint
        
        Returns:
            Dados do endpoint solicitado.
        """
        try:
            params = {"formato": formato}
            if filters:
                params.update(filters)
            
            params = {k: v for k, v in params.items() if v is not None}
            
            request = validate_request_parameters(endpoint, params)
            
            client = await get_client()
            data = await client.fetch_data(request)
            
            metadata = {
                "endpoint": endpoint,
                "formato": formato,
                "filtros_aplicados": {k: v for k, v in params.items() if k != "formato"}
            }
            
            if isinstance(data, list):
                metadata["total_registros"] = len(data)
            elif isinstance(data, str) and formato == "csv":
                metadata["total_linhas"] = len(data.splitlines())
            
            logger.info(f"Dados do endpoint '{endpoint}' obtidos com sucesso")
            
            return APIResponse(
                success=True,
                data=data,
                metadata=metadata
            )
        
        except Exception as e:
            logger.error(f"Erro ao buscar dados do endpoint '{endpoint}': {e}")
            return APIResponse(
                success=False,
                error=str(e),
                metadata={"endpoint": endpoint}
            )

    @mcp.tool()
    async def health_check() -> Dict[str, Any]:
        """
        Verifica se a API da ALEPE está funcionando corretamente.
        
        Returns:
            Status da API e informações de conectividade.
        """
        try:
            client = await get_client()
            health_info = await client.health_check()
            
            logger.info(f"Health check concluído: {health_info['status']}")
            return health_info
        
        except Exception as e:
            logger.error(f"Erro no health check: {e}")
            return {
                "status": "error",
                "error": str(e),
                "api_url": settings.alepe_base_url
            }

    @mcp.tool()
    async def get_api_info() -> Dict[str, Any]:
        """
        Retorna informações sobre a API da ALEPE e este servidor MCP.
        
        Returns:
            Informações da API e configurações do servidor.
        """
        try:
            return {
                "mcp_server": {
                    "name": "ALEPE Data Access",
                    "version": "0.1.0",
                    "description": "Servidor MCP para acesso aos dados abertos da ALEPE"
                },
                "api_alepe": {
                    "base_url": settings.alepe_base_url,
                    "supported_formats": settings.supported_formats,
                    "available_endpoints": settings.available_endpoints,
                    "rate_limit": f"{settings.rate_limit_requests} requisições/minuto"
                },
                "configuration": {
                    "timeout": settings.timeout,
                    "max_retries": settings.max_retries,
                    "retry_delay": settings.retry_delay,
                    "user_agent": settings.user_agent
                }
            }
        
        except Exception as e:
            logger.error(f"Erro ao obter informações da API: {e}")
            return {
                "error": str(e)
            }
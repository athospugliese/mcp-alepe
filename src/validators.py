"""
Validadores para os parâmetros da API da ALEPE.
"""
from typing import Any, Dict, List, Optional, Union, Literal
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import re

from src.config import ENDPOINT_FILTERS, FILTER_VALIDATIONS, settings


class APIRequest(BaseModel):
    """Modelo base para requisições à API da ALEPE."""
    
    endpoint: str = Field(..., description="Endpoint da API")
    formato: str = Field(default="json", description="Formato dos dados (json ou csv)")
    filters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Filtros adicionais")
    
    @field_validator("endpoint")
    @classmethod
    def validate_endpoint(cls, v: str) -> str:
        """Valida se o endpoint é suportado."""
        if v not in settings.available_endpoints:
            raise ValueError(
                f"Endpoint '{v}' não suportado. "
                f"Endpoints disponíveis: {list(settings.available_endpoints.keys())}"
            )
        return v
    
    @field_validator("formato")
    @classmethod
    def validate_formato(cls, v: str) -> str:
        """Valida o formato dos dados."""
        if v.lower() not in settings.supported_formats:
            raise ValueError(
                f"Formato '{v}' não suportado. "
                f"Formatos disponíveis: {settings.supported_formats}"
            )
        return v.lower()
    
    @field_validator("filters")
    @classmethod
    def validate_filters(cls, v: Dict[str, Any], info) -> Dict[str, Any]:
        """Valida os filtros baseado no endpoint."""
        if not v:
            return v
            
        endpoint = info.data.get("endpoint") if info else None
        if not endpoint:
            return v
        
        # Verifica se os filtros são válidos para o endpoint
        valid_filters = ENDPOINT_FILTERS.get(endpoint, [])
        
        for filter_key, filter_value in v.items():
            # Verifica se o filtro é válido para o endpoint
            if valid_filters and filter_key not in valid_filters and filter_key != "formato":
                raise ValueError(
                    f"Filtro '{filter_key}' não válido para endpoint '{endpoint}'. "
                    f"Filtros válidos: {valid_filters}"
                )
            
            # Aplica validações específicas
            if filter_key in FILTER_VALIDATIONS:
                validation = FILTER_VALIDATIONS[filter_key]
                
                if callable(validation):
                    try:
                        if not validation(filter_value):
                            raise ValueError(f"Valor inválido para filtro '{filter_key}': {filter_value}")
                    except (ValueError, TypeError):
                        raise ValueError(f"Valor inválido para filtro '{filter_key}': {filter_value}")
                
                elif isinstance(validation, list):
                    if filter_value not in validation:
                        raise ValueError(
                            f"Valor '{filter_value}' inválido para filtro '{filter_key}'. "
                            f"Valores válidos: {validation}"
                        )
        
        return v


class ParlamentarRequest(APIRequest):
    """Requisição específica para dados de parlamentares."""
    
    endpoint: Literal["parlamentares"] = "parlamentares"
    partido: Optional[str] = Field(None, description="Sigla do partido")
    situacao: Optional[str] = Field(None, description="Situação do parlamentar (ativo/inativo)")
    legislatura: Optional[int] = Field(None, description="Número da legislatura")
    
    @field_validator("partido")
    @classmethod
    def validate_partido(cls, v: Optional[str]) -> Optional[str]:
        """Valida a sigla do partido."""
        if v and not re.match(r"^[A-Z]{2,10}$", v):
            raise ValueError("Sigla do partido deve conter apenas letras maiúsculas (2-10 caracteres)")
        return v
    
    @field_validator("legislatura")
    @classmethod
    def validate_legislatura(cls, v: Optional[int]) -> Optional[int]:
        """Valida o número da legislatura."""
        if v and (v < 1 or v > 20):
            raise ValueError("Legislatura deve estar entre 1 e 20")
        return v


class ServidorRequest(APIRequest):
    """Requisição específica para dados de servidores."""
    
    endpoint: Literal["servidores"] = "servidores"
    vinculo: Optional[str] = Field(None, description="Tipo de vínculo")
    situacao: Optional[str] = Field(None, description="Situação do servidor")
    cargo: Optional[str] = Field(None, description="Cargo do servidor")
    lotacao: Optional[str] = Field(None, description="Lotação do servidor")


class ContratoRequest(APIRequest):
    """Requisição específica para dados de contratos."""
    
    endpoint: Literal["contratos"] = "contratos"
    ano: Optional[int] = Field(None, description="Ano do contrato")
    valor_min: Optional[float] = Field(None, description="Valor mínimo do contrato")
    valor_max: Optional[float] = Field(None, description="Valor máximo do contrato")
    fornecedor: Optional[str] = Field(None, description="Nome ou CNPJ do fornecedor")
    
    @field_validator("ano")
    @classmethod
    def validate_ano(cls, v: Optional[int]) -> Optional[int]:
        """Valida o ano do contrato."""
        current_year = datetime.now().year
        if v and (v < 2000 or v > current_year):
            raise ValueError(f"Ano deve estar entre 2000 e {current_year}")
        return v
    
    @field_validator("valor_min", "valor_max")
    @classmethod
    def validate_valores(cls, v: Optional[float]) -> Optional[float]:
        """Valida os valores dos contratos."""
        if v and v < 0:
            raise ValueError("Valores devem ser positivos")
        return v


class LicitacaoRequest(APIRequest):
    """Requisição específica para dados de licitações."""
    
    endpoint: Literal["licitacoes"] = "licitacoes"
    ano: Optional[int] = Field(None, description="Ano da licitação")
    modalidade: Optional[str] = Field(None, description="Modalidade da licitação")
    situacao: Optional[str] = Field(None, description="Situação da licitação")
    
    @field_validator("ano")
    @classmethod
    def validate_ano(cls, v: Optional[int]) -> Optional[int]:
        """Valida o ano da licitação."""
        current_year = datetime.now().year
        if v and (v < 2000 or v > current_year):
            raise ValueError(f"Ano deve estar entre 2000 e {current_year}")
        return v


class RemuneracaoRequest(APIRequest):
    """Requisição específica para dados de remuneração."""
    
    endpoint: Literal["remuneracao"] = "remuneracao"
    ano: Optional[int] = Field(None, description="Ano da remuneração")
    mes: Optional[int] = Field(None, description="Mês da remuneração")
    vinculo: Optional[str] = Field(None, description="Tipo de vínculo")
    
    @field_validator("ano")
    @classmethod
    def validate_ano(cls, v: Optional[int]) -> Optional[int]:
        """Valida o ano da remuneração."""
        current_year = datetime.now().year
        if v and (v < 2000 or v > current_year):
            raise ValueError(f"Ano deve estar entre 2000 e {current_year}")
        return v
    
    @field_validator("mes")
    @classmethod
    def validate_mes(cls, v: Optional[int]) -> Optional[int]:
        """Valida o mês da remuneração."""
        if v and (v < 1 or v > 12):
            raise ValueError("Mês deve estar entre 1 e 12")
        return v


def validate_request_parameters(
    endpoint: str, 
    parameters: Dict[str, Any]
) -> Union[APIRequest, ParlamentarRequest, ServidorRequest, ContratoRequest, LicitacaoRequest, RemuneracaoRequest]:
    """
    Valida os parâmetros da requisição baseado no endpoint.
    
    Args:
        endpoint: Nome do endpoint
        parameters: Parâmetros da requisição
        
    Returns:
        Objeto validado da requisição
        
    Raises:
        ValueError: Se os parâmetros são inválidos
    """
    # Mapeia endpoints para suas classes de validação específicas
    request_classes = {
        "parlamentares": ParlamentarRequest,
        "servidores": ServidorRequest,
        "contratos": ContratoRequest,
        "licitacoes": LicitacaoRequest,
        "remuneracao": RemuneracaoRequest,
    }
    
    # Use a classe específica se disponível, senão use a classe base
    request_class = request_classes.get(endpoint, APIRequest)
    
    # Adiciona o endpoint aos parâmetros se não estiver presente
    if "endpoint" not in parameters:
        parameters["endpoint"] = endpoint
    
    # Valida e retorna a requisição
    return request_class(**parameters)


def build_query_params(request: APIRequest) -> Dict[str, str]:
    """
    Constrói os parâmetros de query para a URL da API.
    
    Args:
        request: Objeto da requisição validada
        
    Returns:
        Dicionário com os parâmetros de query
    """
    params = {"formato": request.formato}
    
    # Adiciona filtros específicos baseado no tipo da requisição
    if isinstance(request, ParlamentarRequest):
        if request.partido:
            params["partido"] = request.partido
        if request.situacao:
            params["situacao"] = request.situacao
        if request.legislatura:
            params["legislatura"] = str(request.legislatura)
    
    elif isinstance(request, ServidorRequest):
        if request.vinculo:
            params["vinculo"] = request.vinculo
        if request.situacao:
            params["situacao"] = request.situacao
        if request.cargo:
            params["cargo"] = request.cargo
        if request.lotacao:
            params["lotacao"] = request.lotacao
    
    elif isinstance(request, ContratoRequest):
        if request.ano:
            params["ano"] = str(request.ano)
        if request.valor_min:
            params["valor_min"] = str(request.valor_min)
        if request.valor_max:
            params["valor_max"] = str(request.valor_max)
        if request.fornecedor:
            params["fornecedor"] = request.fornecedor
    
    elif isinstance(request, LicitacaoRequest):
        if request.ano:
            params["ano"] = str(request.ano)
        if request.modalidade:
            params["modalidade"] = request.modalidade
        if request.situacao:
            params["situacao"] = request.situacao
    
    elif isinstance(request, RemuneracaoRequest):
        if request.ano:
            params["ano"] = str(request.ano)
        if request.mes:
            params["mes"] = str(request.mes)
        if request.vinculo:
            params["vinculo"] = request.vinculo
    
    # Adiciona filtros genéricos
    if request.filters:
        for key, value in request.filters.items():
            if key != "formato":  # formato já foi adicionado
                params[key] = str(value)
    
    return params
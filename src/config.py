"""
Configurações para o MCP Server da ALEPE.
"""
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Configurações da aplicação."""
    
    # API da ALEPE
    alepe_base_url: str = Field(
        default="https://dadosabertos.alepe.pe.gov.br/api/v1",
        description="URL base da API da ALEPE"
    )
    
    # HTTP Client
    timeout: float = Field(
        default=30.0,
        description="Timeout para requisições HTTP em segundos"
    )
    
    max_retries: int = Field(
        default=3,
        description="Número máximo de tentativas para requisições HTTP"
    )
    
    retry_delay: float = Field(
        default=1.0,
        description="Delay entre tentativas em segundos"
    )
    
    # Rate limiting
    rate_limit_requests: int = Field(
        default=60,
        description="Número máximo de requisições por minuto"
    )
    
    # User Agent
    user_agent: str = Field(
        default="MCP-ALEPE/0.1.0 (Data Access Tool)",
        description="User Agent para requisições HTTP"
    )
    
    # Formatos suportados
    supported_formats: list[str] = Field(
        default=["json", "csv"],
        description="Formatos de dados suportados pela API"
    )
    
    # Endpoints disponíveis
    available_endpoints: dict[str, str] = Field(
        default={
            "parlamentares": "Dados dos deputados estaduais",
            "cargos": "Cargos disponíveis na ALEPE",
            "lotacoes": "Lotações organizacionais",
            "servidores": "Dados dos servidores públicos",
            "remuneracao": "Informações de remuneração",
            "licitacoes": "Processos licitatórios",
            "contratos": "Contratos firmados"
        },
        description="Endpoints disponíveis na API da ALEPE"
    )
    
    # Log level
    log_level: str = Field(
        default="INFO",
        description="Nível de log da aplicação"
    )
    
    class Config:
        env_prefix = "ALEPE_"
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instância global das configurações
settings = Settings()


def get_settings() -> Settings:
    """Retorna as configurações da aplicação."""
    return settings


# Constantes úteis
API_VERSION = "v1"
DEFAULT_FORMAT = "json"
MAX_ITEMS_PER_REQUEST = 1000

# Filtros comuns por endpoint
ENDPOINT_FILTERS = {
    "parlamentares": ["partido", "situacao", "legislatura"],
    "servidores": ["vinculo", "situacao", "cargo", "lotacao"],
    "contratos": ["ano", "valor_min", "valor_max", "fornecedor"],
    "licitacoes": ["ano", "modalidade", "situacao"],
    "remuneracao": ["ano", "mes", "vinculo"]
}

# Validações de filtros
FILTER_VALIDATIONS = {
    "formato": ["json", "csv"],
    "situacao": ["ativo", "inativo"],
    "vinculo": ["efetivo", "comissionado", "terceirizado", "estagiario"],
    "ano": lambda x: 2000 <= int(x) <= 2025,
    "mes": lambda x: 1 <= int(x) <= 12
}
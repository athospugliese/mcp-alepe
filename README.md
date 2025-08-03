# MCP ALEPE

Servidor MCP (Model Context Protocol) para acesso aos dados abertos da Assembleia Legislativa de Pernambuco (ALEPE).

## 📋 Descrição

Este projeto fornece um servidor MCP que permite acesso programático aos dados abertos da ALEPE através de uma interface padronizada. O servidor oferece ferramentas para buscar informações sobre parlamentares, servidores, contratos, licitações e outros dados públicos.

## 🚀 Funcionalidades

- ✅ Acesso a todos os endpoints da API da ALEPE
- ✅ Suporte aos formatos JSON e CSV
- ✅ Validação robusta de parâmetros
- ✅ Rate limiting inteligente
- ✅ Retry automático com backoff exponencial
- ✅ Health check da API
- ✅ Logging detalhado
- ✅ Configuração via variáveis de ambiente

## 📦 Instalação

### Pré-requisitos

- Python >= 3.10
- [uv](https://github.com/astral-sh/uv) (recomendado para gerenciamento de dependências)

### Instalação com uv

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/mcp-alepe.git
cd mcp-alepe

# Instale as dependências
uv pip install -e .

# Para desenvolvimento
uv pip install -e ".[dev]"
```

### Instalação alternativa com pip

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/mcp-alepe.git
cd mcp-alepe

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -e .

# Para desenvolvimento
pip install -e ".[dev]"
```

## ⚙️ Configuração

O servidor pode ser configurado através de variáveis de ambiente com o prefixo `ALEPE_`:

```bash
# URL base da API (padrão: https://dadosabertos.alepe.pe.gov.br/api/v1)
ALEPE_BASE_URL=https://dadosabertos.alepe.pe.gov.br/api/v1

# Timeout para requisições em segundos (padrão: 30.0)
ALEPE_TIMEOUT=30.0

# Número máximo de tentativas (padrão: 3)
ALEPE_MAX_RETRIES=3

# Rate limit - requisições por minuto (padrão: 60)
ALEPE_RATE_LIMIT_REQUESTS=60

# Nível de log (padrão: INFO)
ALEPE_LOG_LEVEL=INFO

# User Agent personalizado
ALEPE_USER_AGENT="MCP-ALEPE/0.1.0 (Custom Tool)"
```

Ou crie um arquivo `.env` na raiz do projeto:

```env
ALEPE_LOG_LEVEL=DEBUG
ALEPE_TIMEOUT=45.0
ALEPE_RATE_LIMIT_REQUESTS=90
```

## 🔧 Uso

### Executando o servidor

```bash
# Execução normal
python -m src.main

# Modo de desenvolvimento (com logs DEBUG)
python -m src.main --dev

# Ou usando o script instalado
mcp-alepe
```

### Ferramentas disponíveis

O servidor MCP oferece as seguintes ferramentas:

#### 1. `list_available_endpoints`
Lista todos os endpoints disponíveis na API da ALEPE.

#### 2. `get_parlamentares`
Busca dados dos deputados estaduais.
```python
# Parâmetros opcionais:
# - formato: "json" ou "csv"
# - partido: sigla do partido (ex: "PT", "PSDB")
# - situacao: "ativo" ou "inativo"
# - legislatura: número da legislatura
```

#### 3. `get_servidores`
Busca dados dos servidores públicos.
```python
# Parâmetros opcionais:
# - formato: "json" ou "csv"
# - vinculo: "efetivo", "comissionado", "terceirizado", "estagiario"
# - situacao: "ativo" ou "inativo"
# - cargo: nome do cargo
# - lotacao: lotação organizacional
```

#### 4. `get_contratos`
Busca dados dos contratos.
```python
# Parâmetros opcionais:
# - formato: "json" ou "csv"
# - ano: ano do contrato
# - valor_min: valor mínimo
# - valor_max: valor máximo
# - fornecedor: nome ou CNPJ do fornecedor
```

#### 5. `get_licitacoes`
Busca dados das licitações.
```python
# Parâmetros opcionais:
# - formato: "json" ou "csv"
# - ano: ano da licitação
# - modalidade: modalidade da licitação
# - situacao: situação da licitação
```

#### 6. `get_remuneracao`
Busca dados de remuneração.
```python
# Parâmetros opcionais:
# - formato: "json" ou "csv"
# - ano: ano da remuneração
# - mes: mês (1-12)
# - vinculo: tipo de vínculo
```

#### 7. `get_cargos`
Busca dados dos cargos disponíveis.

#### 8. `get_lotacoes`
Busca dados das lotações organizacionais.

#### 9. `search_data`
Busca dados de qualquer endpoint com filtros personalizados.
```python
# Parâmetros:
# - endpoint: nome do endpoint
# - formato: "json" ou "csv"
# - **filters: filtros específicos
```

#### 10. `health_check`
Verifica se a API está funcionando.

#### 11. `get_api_info`
Retorna informações sobre a API e o servidor MCP.

## 🏗️ Estrutura do Projeto

```
mcp-alepe/
├── src/
│   ├── alepe_tools.py    # Ferramentas MCP
│   ├── config.py         # Configurações
│   ├── http_client.py    # Cliente HTTP
│   ├── main.py          # Ponto de entrada
│   └── validators.py     # Validadores
├── tests/               # Testes (a implementar)
├── pyproject.toml       # Configuração do projeto
├── README.md           # Este arquivo
└── .env.example        # Exemplo de configuração
```

## 🧪 Desenvolvimento

### Configurando o ambiente de desenvolvimento

```bash
# Clone e instale as dependências de desenvolvimento
git clone https://github.com/seu-usuario/mcp-alepe.git
cd mcp-alepe
uv pip install -e ".[dev]"
```

### Executando testes

```bash
# Execute todos os testes
pytest

# Com cobertura
pytest --cov=src --cov-report=html

# Testes específicos
pytest tests/test_validators.py -v
```

### Formatação e linting

```bash
# Formatação com black
black src/ tests/

# Ordenação de imports
isort src/ tests/

# Linting com flake8
flake8 src/ tests/

# Verificação de tipos com mypy
mypy src/
```

### Executando em modo de desenvolvimento

```bash
# Com logs detalhados
python -m src.main --dev
```

## 📊 Exemplos de Uso

### Exemplo 1: Buscar deputados de um partido específico

```python
# A ferramenta get_parlamentares seria chamada com:
{
    "formato": "json",
    "partido": "PT",
    "situacao": "ativo"
}

# Retorna:
{
    "success": true,
    "data": [
        {
            "id": 1,
            "nome": "Deputado Exemplo",
            "partido": "PT",
            "situacao": "ativo",
            "legislatura": 19
        }
    ],
    "metadata": {
        "endpoint": "parlamentares",
        "formato": "json",
        "filtros_aplicados": {
            "partido": "PT",
            "situacao": "ativo"
        },
        "total_registros": 1
    }
}
```

### Exemplo 2: Buscar contratos por valor

```python
# A ferramenta get_contratos seria chamada com:
{
    "formato": "json",
    "ano": 2024,
    "valor_min": 100000.0,
    "valor_max": 500000.0
}

# Retorna contratos entre R$ 100.000 e R$ 500.000 em 2024
```

### Exemplo 3: Health check

```python
# A ferramenta health_check retorna:
{
    "status": "healthy",
    "api_url": "https://dadosabertos.alepe.pe.gov.br/api/v1",
    "response_time_seconds": 0.234,
    "available_endpoints": [
        "parlamentares",
        "servidores",
        "contratos",
        "licitacoes",
        "remuneracao",
        "cargos",
        "lotacoes"
    ]
}
```

## 🔍 Monitoramento e Logs

O servidor gera logs detalhados para monitoramento:

```
2024-08-03 10:30:15 - src.main - INFO - Iniciando servidor MCP da ALEPE
2024-08-03 10:30:15 - src.http_client - INFO - Cliente HTTP inicializado
2024-08-03 10:30:16 - src.main - INFO - ✅ API da ALEPE está acessível (tempo de resposta: 0.234s)
2024-08-03 10:30:16 - src.main - INFO - 🚀 Servidor MCP da ALEPE iniciado com sucesso
2024-08-03 10:30:20 - src.alepe_tools - INFO - Dados de parlamentares obtidos com sucesso
```

## ⚡ Performance e Limitações

### Rate Limiting
- Padrão: 60 requisições por minuto
- Implementação: Token bucket algorithm
- Configurável via `ALEPE_RATE_LIMIT_REQUESTS`

### Retry Logic
- Máximo de 3 tentativas por padrão
- Backoff exponencial (1s, 2s, 4s)
- Configurável via `ALEPE_MAX_RETRIES` e `ALEPE_RETRY_DELAY`

### Timeouts
- Padrão: 30 segundos por requisição
- Configurável via `ALEPE_TIMEOUT`

## 🛠️ Troubleshooting

### Problemas Comuns

#### 1. Erro de conexão
```
Erro de conexão com a API da ALEPE: Connection timeout
```
**Solução:** Verifique sua conexão com a internet e aumente o timeout:
```bash
export ALEPE_TIMEOUT=60.0
```

#### 2. Rate limit atingido
```
Rate limit atingido, aguardando 2.5s
```
**Solução:** Normal, o sistema aguarda automaticamente. Para reduzir:
```bash
export ALEPE_RATE_LIMIT_REQUESTS=30
```

#### 3. Dados não encontrados
```
Erro na API da ALEPE (HTTP 404): Endpoint não encontrado
```
**Solução:** Verifique se o endpoint está correto:
```python
# Use list_available_endpoints para ver endpoints válidos
```

#### 4. Parâmetros inválidos
```
Valor 'INVALID' inválido para filtro 'situacao'. Valores válidos: ['ativo', 'inativo']
```
**Solução:** Use apenas valores válidos conforme documentação.

### Debug

Para debug detalhado:

```bash
# Ative logs DEBUG
export ALEPE_LOG_LEVEL=DEBUG
python -m src.main --dev
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Padrões de Código

- Use `black` para formatação
- Use `isort` para ordenação de imports
- Use `mypy` para verificação de tipos
- Mantenha cobertura de testes > 80%
- Adicione docstrings para funções públicas

## 📝 Changelog

### v0.1.0 (2024-08-03)
- ✅ Implementação inicial
- ✅ Suporte a todos os endpoints da ALEPE
- ✅ Validação robusta de parâmetros
- ✅ Rate limiting e retry logic
- ✅ Logging estruturado
- ✅ Configuração via ambiente

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [ALEPE](https://www.alepe.pe.gov.br/) por disponibilizar os dados abertos
- [FastMCP](https://github.com/jlowin/fastmcp) pelo framework MCP
- Comunidade Python pela excelente ecosistema de bibliotecas

## 📞 Suporte

- 📧 Email: seu.email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/seu-usuario/mcp-alepe/issues)
- 📖 Documentação: [Wiki do Projeto](https://github.com/seu-usuario/mcp-alepe/wiki)

## 🔗 Links Úteis

- [API da ALEPE](https://dadosabertos.alepe.pe.gov.br/)
- [Portal da ALEPE](https://www.alepe.pe.gov.br/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)

---

Feito com ❤️ para promover transparência e acesso aos dados públicos de Pernambuco.
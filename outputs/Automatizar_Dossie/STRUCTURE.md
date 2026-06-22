# 📦 Estrutura Completa do Projeto

Guia visual de cada arquivo, pasta e sua responsabilidade.

---

## 🌳 Árvore de Diretórios

```
Automatizar_Dossie/
│
├── 📄 main.py                          ⭐ Entry point raiz (redireciona para app/main.py)
├── 📄 requirements.txt                 Dependências Python (pip install -r requirements.txt)
├── 📄 pyproject.toml                   Metadados do projeto (versão, dependências opcionais)
├── 📄 Makefile                         Atalhos para tarefas comuns (make help)
├── 📄 .gitignore                       Ignora __pycache__, .env, venv/, etc no Git
│
├── 📚 README.md                        ⭐ Guia principal do projeto
├── 📚 CONTRIBUTING.md                  Como contribuir (issues, PRs, padrões)
├── 📚 DEVELOPMENT.md                   Guia técnico (como estender/modificar)
├── 📚 CHANGELOG.md                     Histórico de versões
├── 📚 STRUCTURE.md                     Este arquivo
│
├── 🗂️ .devcontainer/
│   └── devcontainer.json               Configuração VS Code Dev Container
│
├── 🗂️ .streamlit/
│   └── config.toml                     Configurações da interface Streamlit
│
├── 🗂️ app/                             🎯 CÓDIGO PRINCIPAL
│   ├── __init__.py                     Marca como pacote Python
│   ├── main.py                         ⭐ Interface Streamlit (UI)
│   │
│   ├── 🗂️ core/                        Lógica de negócio
│   │   ├── __init__.py
│   │   ├── automation.py               🔧 DossieAutomation — orquestração principal
│   │   └── file_processor.py           🔧 FileProcessor — processamento PDF/DOCX
│   │
│   └── 🗂️ utils/                       Utilitários e helpers
│       ├── __init__.py
│       ├── helpers.py                  🔧 Formatação (CNPJ, CPF) + validações
│       └── logger.py                   🔧 Logging centralizado (loguru)
│
├── 🗂️ config/                          ⚙️ CONFIGURAÇÃO
│   ├── __init__.py
│   ├── settings.py                     🔧 Variáveis de ambiente + caminhos
│   └── constants.py                    🔧 Constantes estáticas (MESES_PT, placeholders)
│
└── 🗂️ tests/                           🧪 TESTES
    ├── __init__.py
    ├── test_file_processor.py           Testes para FileProcessor
    └── test_automation.py               Testes para DossieAutomation

# Arquivos gerados em tempo de execução (não commitados):
template_base_ofc.docx                 Template DOCX com Jinja2 (envio manual)
.env                                   Variáveis de ambiente (create manually)
logs/app.log                           Arquivo de log (gerado automaticamente)
```

---

## 📄 Arquivo por Arquivo

### 🎯 Raiz do Projeto

#### `main.py` — Entry Point
```python
"""Entry point raiz — redireciona para app/main.py."""
from app.main import *  # noqa: F401, F403
```
- **Função:** Permite rodar `streamlit run main.py` em vez de `streamlit run app/main.py`
- **Quando modificar:** Raramente
- **Dependências:** app/main.py

#### `requirements.txt` — Dependências
```
streamlit==1.28.1
docxtpl==0.16.6
python-docx==0.8.11
...
```
- **Função:** Lista todas as bibliotecas necessárias
- **Quando modificar:** Sempre que adicionar/remover library
- **Comando:** `pip install -r requirements.txt`
- **Atualizar:** `pip freeze > requirements.txt`

#### `pyproject.toml` — Metadados
```toml
[project]
name = "automatizar-dossie"
version = "1.1.0"
...
```
- **Função:** Configuração PEP 518 (build system, deps, tools)
- **Quando modificar:** Quando mudar versão ou adicionar dev-tools
- **Contém:**
  - Versão do projeto
  - Dependências opcionais (`[dev]`)
  - Config de Black, Ruff, pytest, mypy

#### `Makefile` — Automação de Tarefas
```makefile
help:
  @echo "Tarefas disponíveis"

install:
  pip install -r requirements.txt

run:
  streamlit run main.py
```
- **Função:** Atalhos para comandos comuns
- **Quando modificar:** Ao adicionar novas tarefas
- **Usar:** `make help`, `make install`, `make run`, `make test`

#### `.gitignore` — Ignorar Arquivos
```
__pycache__/
.env
venv/
logs/
*.log
```
- **Função:** Diz ao Git quais arquivos não committar
- **Quando modificar:** Raramente (quando adicionar novo tipo de arquivo temporário)

---

### 📚 Documentação

#### `README.md` — Guia Principal
- ✅ Visão geral do projeto
- ✅ Como instalar
- ✅ Como usar (interface)
- ✅ Stack tecnológico
- ✅ Troubleshooting

**Primeira coisa que alguém lê!**

#### `CONTRIBUTING.md` — Para Contribuidores
- Como reportar bugs
- Como sugerir features
- Padrões de código
- Processo de PR

**Essencial para open-source.**

#### `DEVELOPMENT.md` — Guia Técnico
- 📝 Exemplos práticos (XLS, validações)
- 📝 Como editar o template DOCX
- 📝 Como estender funcionalidades
- 📝 Debugging e logging

**Para quem vai **modificar** o código.**

#### `CHANGELOG.md` — Histórico
- Lista de mudanças por versão
- Added / Changed / Fixed / Removed
- Links para releases

**Para rastrear evolução do projeto.**

#### `STRUCTURE.md` — Este Arquivo
- Visão geral da estrutura
- Explicação de cada arquivo
- Guia de navegação

---

### 🔧 Configuração

#### `config/settings.py` — Variáveis de Ambiente
```python
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = BASE_DIR / "template_base_ofc.docx"
N8N_WEBHOOK_URL = os.environ.get("N8N_WEBHOOK_URL", "...")
PDF_DPI = int(os.environ.get("PDF_DPI", "200"))
MAX_UPLOAD_SIZE_BYTES = 50 * 1024 * 1024
```

**Responsabilidades:**
- Ler variáveis de `.env` ou valores padrão
- Definir caminhos (TEMPLATE_PATH, TEMP_DIR)
- Limites (MAX_UPLOAD_SIZE_BYTES)
- Integrações (N8N_WEBHOOK_URL)

**Quando modificar:**
- Adicionar nova integração? → Novo env var aqui
- Mudar limite de upload? → Edite MAX_UPLOAD_SIZE_BYTES

#### `config/constants.py` — Constantes Estáticas
```python
MESES_PT = {1: "Janeiro", 2: "Fevereiro", ...}
PLACEHOLDER_DRE = "[[DEMONSTR_RESULTADO]]"
UPLOAD_KEYS = {"balanco": "balanco_file", ...}
```

**Responsabilidades:**
- Constantes que nunca mudam
- Dicts e listas estáticas
- Placeholders do template

**Quando modificar:**
- Adicionar novo mês ou idioma? → MESES_PT
- Novo placeholder no template? → PLACEHOLDER_*
- Novo tipo de upload? → UPLOAD_KEYS

---

### 🎯 Aplicação

#### `app/main.py` — Interface Streamlit (UI)
```python
st.title("📄 Gerador Automático de Dossiês Contábeis")

tab1, tab2, tab3 = st.tabs(["Dados da Empresa", "Sócios", "Upload"])
# ... abas com inputs

if st.button("✅ GERAR DOSSIÊ"):
    automation = DossieAutomation()
    file_bytes, error = automation.generate(input_data)
    # ... download + n8n
```

**Responsabilidades:**
- Interface com Streamlit (UI)
- Capturar inputs do usuário
- Chamar `DossieAutomation.generate()`
- Exibir resultados

**Estrutura:**
1. 3 abas (Empresa, Sócios, Upload)
2. Inputs e formatação
3. Botão de geração
4. Download + integração n8n

**Quando modificar:**
- Mudar layout? Edite aqui
- Adicionar novo campo? Crie input + adicione a input_data
- Mudar fluxo? Edite lógica do botão

**⚠️ Evite:** Lógica pesada aqui (use core/)

---

#### `app/core/automation.py` — Orquestração Principal
```python
class DossieAutomation:
    def generate(self, input_data: dict) -> tuple[Optional[bytes], Optional[str]]:
        """Gera dossiê completo."""
        # 1. Salvar uploads em disco
        # 2. Renderizar template
        # 3. Inserir PDFs/DOCXs
        # 4. Retornar DOCX gerado
    
    def send_to_n8n(self, input_data, file_bytes) -> tuple[bool, str]:
        """Envia para webhook n8n."""
        ...
```

**Responsabilidades:**
- Orquestração: coordena FileProcessor + arquivo final
- Tratamento de erros e logging
- Integração n8n

**Quando modificar:**
- Mudar fluxo de geração? Edite `generate()`
- Adicionar nova integração? Novo método aqui
- Mudar dados no contexto? Edite contexto no `_render_template()`

---

#### `app/core/file_processor.py` — Processamento de Arquivos
```python
class FileProcessor:
    def validate_file(self, filename: str) -> bool:
        """Valida extensão."""
    
    def pdf_to_images(self, pdf_path: str) -> list[bytes]:
        """Converte PDF em PNGs."""
    
    def insert_pdf_at_placeholder(self, doc, placeholder, pdf_path) -> bool:
        """Substitui placeholder por imagens."""
    
    def insert_docx_at_placeholder(self, doc, placeholder, docx_path) -> bool:
        """Substitui placeholder por conteúdo DOCX."""
```

**Responsabilidades:**
- PDF → imagens (usando PyMuPDF)
- Inserção de imagens/conteúdo em DOCX
- Validação de arquivos
- Cleanup de temporários

**Quando modificar:**
- Suportar novo formato (XLS, PPTX)? Novo método aqui
- Mudar DPI/tamanho de imagens? Edite `pdf_to_images()`
- Mudar estratégia de inserção? Edite `insert_*_at_placeholder()`

---

#### `app/utils/helpers.py` — Formatação e Validação
```python
def clean_numbers(text: str) -> str:
    """Remove não-numéricos."""

def format_cnpj(cnpj: str) -> str:
    """Formata CNPJ: XX.XXX.XXX/XXXX-XX."""

def format_cpf(cpf: str) -> str:
    """Formata CPF: XXX.XXX.XXX-XX."""

def validate_cpf(cpf: str) -> bool:
    """Valida CPF (algoritmo módulo 11)."""

def build_periodo_em_data(data_inicio, data_fim) -> str:
    """Constrói string curta: '01 a 12/24'."""
```

**Responsabilidades:**
- Funções puras (sem efeito colateral)
- Formatação de strings
- Validações (CPF, CNPJ)

**Quando modificar:**
- Adicionar validação? Novo função aqui
- Mudar formato? Edite função correspondente
- Adicionar idioma? Novo método (ex: `format_cpf_en()`)

**⚠️ Regra:** Funções devem ser **puras** (input → output, sem estado)

---

#### `app/utils/logger.py` — Logging Centralizado
```python
from loguru import logger

logger.remove()  # Remove handler padrão
logger.add(sys.stderr, level="INFO", ...)
logger.add("logs/app.log", rotation="00:00", ...)
```

**Responsabilidades:**
- Configuração centralizada de logging
- Console + arquivo (rotativo)
- Formato consistente

**Quando modificar:**
- Mudar nível padrão? Edite `level="INFO"`
- Adicionar novo sink? Novo `logger.add()`
- Mudar formato? Edite `format="..."`

**Usar:**
```python
from app.utils.logger import logger
logger.info("Algo aconteceu")
logger.error(f"Erro: {exc}")
```

---

### 🧪 Testes

#### `tests/test_file_processor.py` — Testes do FileProcessor
```python
class TestFileProcessor:
    @pytest.fixture
    def processor(self):
        return FileProcessor()
    
    def test_validate_file_docx(self, processor):
        assert processor.validate_file("arquivo.docx") is True
    
    def test_validate_file_invalid(self, processor):
        assert processor.validate_file("arquivo.exe") is False
```

**Cobertura:**
- ✅ `validate_file()`
- ✅ `save_upload_to_temp()`
- ✅ `cleanup_temp_files()`
- ✅ `pdf_balanco_duas_paginas()` (erro se < 2 pages)

**Quando adicionar testes:**
- Nova função em FileProcessor? Teste aqui
- Nova validação? Teste aqui

#### `tests/test_automation.py` — Testes da Automação
```python
@pytest.fixture
def automation():
    return DossieAutomation()

def test_generate_returns_error_if_upload_missing(self, automation, base_input):
    base_input["uploads"]["balanco_file"] = None
    file_bytes, error = automation.generate(base_input)
    assert error is not None
```

**Cobertura:**
- ✅ `generate()` com upload faltando
- ✅ `send_to_n8n()` desabilitado
- ✅ `send_to_n8n()` com sucesso
- ✅ `send_to_n8n()` com erro

**Quando adicionar testes:**
- Nova lógica em `generate()`? Teste aqui
- Nova integração? Teste aqui

---

### 🔧 Configuração Streamlit

#### `.streamlit/config.toml` — Preferências da Interface
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"

[client]
showErrorDetails = true

[server]
port = 8501
```

**Responsabilidades:**
- Tema (cores, fontes)
- Comportamento da interface
- Porta e host

**Quando modificar:**
- Mudar cores? Edite `[theme]`
- Mudar comportamento? Edite `[client]` ou `[server]`

---

### 🐳 Development Container

#### `.devcontainer/devcontainer.json` — Config VS Code
```json
{
  "name": "Automatizar_Dossie",
  "image": "mcr.microsoft.com/devcontainers/python:3.10",
  "features": {...},
  "postCreateCommand": "pip install -r requirements.txt"
}
```

**Função:** Setup automático de ambiente Python no VS Code
- Abre o projeto em container Docker
- Instala dependências automaticamente
- Configura extensões recomendadas (Black, Ruff)

**Quando usar:**
```bash
# No VS Code, clique em "Reopen in Container"
# Ou execute:
devcontainer open .
```

---

## 🗺️ Mapa de Dependências

```
main.py
  └─ app/main.py (Streamlit UI)
     ├─ app/core/automation.py (DossieAutomation)
     │  ├─ app/core/file_processor.py (FileProcessor)
     │  ├─ config/settings.py
     │  ├─ config/constants.py
     │  └─ app/utils/logger.py
     ├─ app/utils/helpers.py (formatação, validação)
     └─ app/utils/logger.py

tests/test_file_processor.py
  └─ app/core/file_processor.py

tests/test_automation.py
  └─ app/core/automation.py
```

---

## 🎯 Onde Fazer Cada Tipo de Mudança

| Quero... | Arquivo | Motivo |
|----------|---------|--------|
| Adicionar novo campo na UI | `app/main.py` | Interface Streamlit |
| Mudar como CNPJ é formatado | `app/utils/helpers.py` | Função de formatação |
| Adicionar validação de entrada | `app/utils/helpers.py` | Validações centralizadas |
| Processar novo formato (XLS, PPTX) | `app/core/file_processor.py` | Processamento de arquivos |
| Mudar fluxo de geração | `app/core/automation.py` | Orquestração principal |
| Adicionar integração externa (banco, API) | `app/core/automation.py` | Lógica de negócio |
| Mudar tamanho máximo de upload | `config/settings.py` | Configurações |
| Adicionar novo placeholder no template | `config/constants.py` | Constantes |
| Mudar cores da interface | `.streamlit/config.toml` | Tema Streamlit |
| Adicionar nova dependência | `requirements.txt` ou `pyproject.toml` | Dependências |
| Testar uma função | `tests/test_*.py` | Testes unitários |
| Documentar como usar | `README.md` | Guia principal |
| Documentar como modificar | `DEVELOPMENT.md` | Guia técnico |
| Documentar padrões | `CONTRIBUTING.md` | Para contributors |

---

## 📚 Leitura Recomendada por Perfil

### 👤 Usuário Final
- [ ] `README.md` — Como instalar e usar
- [ ] Seção "Como Usar" do README

### 🔧 Desenvolvedor Local
- [ ] `README.md` — Setup inicial
- [ ] `DEVELOPMENT.md` — Como modificar código
- [ ] `CONTRIBUTING.md` — Padrões de código

### 🚀 DevOps / Deploy
- [ ] `README.md` — Pré-requisitos e instalação
- [ ] `pyproject.toml` — Versão, dependências
- [ ] `requirements.txt` — Para pip install
- [ ] `.devcontainer/` — Para containerização

### 📖 Contribuidor Externo
- [ ] `README.md` — Visão geral
- [ ] `CONTRIBUTING.md` — Como contribuir
- [ ] `DEVELOPMENT.md` — Exemplos práticos

---

## 🚀 Próximos Passos após Setup

1. **Leia:** `README.md` (visão geral)
2. **Instale:** `pip install -r requirements.txt`
3. **Configure:** Copie `.env.example` para `.env` (se houver)
4. **Execute:** `streamlit run main.py`
5. **Teste:** `pytest tests/`
6. **Desenvolva:** Veja `DEVELOPMENT.md` para exemplos

---

**Última atualização:** 2024-06-19 | Versão: 1.1.0
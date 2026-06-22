# 📄 Automatizar Dossiê — Gerador de Documentos Contábeis

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Ativo-brightgreen)

Sistema automatizado e modular para geração de **dossiês contábeis profissionais** em formato DOCX, a partir de dados estruturados, balanços em PDF e documentos complementares.

**Demo ao vivo:** [automatizardossie.streamlit.app](https://automatizardossie.streamlit.app/)

---

## 🎯 Visão Geral

Este projeto automatiza a criação de dossiês contábeis completos, combinando:

- **Dados dinâmicos** (empresa, período, sócios/administradores)
- **Balanços e DRE** (em PDF, automaticamente convertidos em imagens)
- **Notas Explicativas** (Markdown → DOCX)
- **Carta de Responsabilidade** (DOCX)
- **Integração n8n** (envia documento e metadados via webhook)

**Resultado:** Um arquivo DOCX pronto para entrega a clientes ou órgãos reguladores.

---

## 🗂️ Estrutura do Projeto

```
Automatizar_Dossie/
├── .devcontainer/                  # Configuração para Dev Container
│   └── devcontainer.json
├── .streamlit/                     # Configuração Streamlit (opcional)
├── app/                            # Código principal da aplicação
│   ├── __init__.py
│   ├── main.py                     # Interface Streamlit (UI)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── automation.py           # Orquestração: geração do dossiê
│   │   └── file_processor.py       # Processamento de PDFs e DOCXs
│   └── utils/
│       ├── __init__.py
│       ├── helpers.py              # Formatação (CNPJ, CPF, datas)
│       └── logger.py               # Logging centralizado (loguru)
├── config/                         # Configurações e constantes
│   ├── __init__.py
│   ├── settings.py                 # Variáveis de ambiente e caminhos
│   └── constants.py                # Constantes estáticas (MESES_PT, placeholders)
├── tests/                          # Testes unitários (pytest)
│   ├── __init__.py
│   ├── test_file_processor.py
│   └── test_automation.py
├── main.py                         # Entry point raiz (redireciona para app/main.py)
├── requirements.txt                # Dependências Python
├── pyproject.toml                  # Metadata do projeto (opcional)
├── .gitignore
└── README.md                       # Este arquivo

# Arquivos adicionados em tempo de execução:
# - template_base_ofc.docx          (template Jinja2 para o dossiê)
```

### Convenções de código

- **Arquivos de configuração:** `config/` — constantes + variáveis de ambiente
- **Lógica de negócio:** `app/core/` — processamento, orquestração
- **Utilitários e helpers:** `app/utils/` — formatação, validação, logging
- **Interface:** `app/main.py` — Streamlit (evite lógica pesada aqui)
- **Testes:** `tests/` — pytest, um arquivo por módulo testado

---

## 🚀 Começando

### Pré-requisitos

- **Python 3.10+**
- **pip** (ou gerenciador de pacotes)
- **Pandoc** (necessário para `pypandoc` converter Markdown)
- **Git** (para controle de versão)

### Instalação do Pandoc

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install pandoc
```

**macOS (Homebrew):**
```bash
brew install pandoc
```

**Windows:**
Baixe em [pandoc.org/installing.html](https://pandoc.org/installing.html) ou use:
```bash
choco install pandoc
```

### Setup local

#### 1. Clone o repositório

```bash
git clone https://github.com/camposs04/Automatizar_Dossie.git
cd Automatizar_Dossie
```

#### 2. Crie um ambiente virtual

```bash
# Linux/macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. Instale as dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Configure variáveis de ambiente (opcional)

Crie um arquivo `.env` na raiz do projeto:

```env
# Integração n8n
N8N_WEBHOOK_URL=https://seu-dominio-n8n.com/webhook/receber-dados
N8N_ENABLED=true

# Processamento de PDF
PDF_DPI=200
IMAGE_WIDTH_INCHES=6

# Logging
LOG_LEVEL=INFO
```

#### 5. Execute a aplicação

```bash
streamlit run main.py
```

A aplicação abrirá em `http://localhost:8501`.

---

## 📖 Como Usar

### Interface Streamlit

A aplicação possui **3 abas**:

#### 🏢 Aba 1: Dados da Empresa / Períodos

- **Nome Fantasia**: Nome comercial da empresa
- **Razão Social**: Nome jurídico completo
- **CNPJ**: Será formatado automaticamente
- **Data de Início / Fim**: Período contábil de referência

#### 👥 Aba 2: Dados dos Sócios / Administradores

- Adicione sócios dinamicamente
- **Nome completo**, **CPF** (formatado automaticamente), **Cargo**
- Remova linhas individuais conforme necessário

#### 📎 Aba 3: Upload de Arquivos

Obrigatório (todos os 4 arquivos):

| Arquivo | Formato | Observação |
|---------|---------|-----------|
| **Balanço Patrimonial** | PDF | Mínimo 2 páginas (pt1 e pt2) |
| **Demonstração do Resultado (DRE)** | PDF | Qualquer número de páginas |
| **Notas Explicativas** | DOCX | **Sem título interno** |
| **Carta de Responsabilidade** | DOCX | **Sem título interno** |

### Resultado

Após preencher e clicar em **✅ GERAR DOSSIÊ CONTÁBIL**:

1. ✅ Download do arquivo `Dossie_Contabil_<EMPRESA>.docx`
2. ➡️ Envio automático para n8n (se habilitado)

---

## 🧪 Testes

### Executar todos os testes

```bash
pytest
```

### Executar com cobertura

```bash
pytest --cov=app --cov-report=html
# Resultado em: htmlcov/index.html
```

### Executar um teste específico

```bash
pytest tests/test_file_processor.py::TestFileProcessor::test_validate_file_docx -v
```

### Testes disponíveis

**`test_file_processor.py`** — Validação e processamento de arquivos:
- `validate_file` — extensões suportadas
- `save_upload_to_temp` — salvar upload em disco
- `cleanup_temp_files` — limpeza segura
- `pdf_balanco_duas_paginas` — extração de 2 páginas do PDF

**`test_automation.py`** — Orquestração:
- `generate` — fluxo completo de geração
- `send_to_n8n` — integração com webhook

---

## 🔧 Guia de Desenvolvimento

### Adicionando uma nova funcionalidade

#### Exemplo: Adicionar suporte a XLS (Balanço em Excel)

1. **Edite `config/constants.py`:**
   ```python
   UPLOAD_KEYS = {
       "balanco": "balanco_file",
       "balanco_xls": "balanco_xls_file",  # ← novo
       ...
   }
   ```

2. **Estenda `app/core/file_processor.py`:**
   ```python
   def xls_to_images(self, xls_path: str) -> list[bytes]:
       """Converte planilha Excel em imagens."""
       # Implementação usando openpyxl + pillow
       ...
   ```

3. **Atualize `app/core/automation.py`:**
   ```python
   def _render_template(self, input_data, temp_paths):
       ...
       # Dentro do contexto:
       balanco_xls_bytes = self._processor.xls_to_images(...)
       context["balanco_xls"] = InlineImage(doc, BytesIO(balanco_xls_bytes), ...)
   ```

4. **Atualize `app/main.py`:**
   ```python
   with col5:
       input_data["uploads"]["balanco_xls_file"] = st.file_uploader(
           "Balanço Patrimonial (XLS)", type=["xls", "xlsx"]
       )
   ```

5. **Adicione testes em `tests/test_file_processor.py`:**
   ```python
   def test_xls_to_images_converts_sheets(self, processor):
       ...
   ```

### Modificando o template DOCX

O arquivo `template_base_ofc.docx` usa **Jinja2** para renderização dinâmica.

**Editar template:**

1. Abra `template_base_ofc.docx` no Microsoft Word ou LibreOffice
2. Os placeholders Jinja2 são inseridos como `{{ variavel }}` ou `{% for ... %}`
3. Exemplos de variáveis disponíveis (em `app/core/automation.py`):
   - `{{ nome_empresa }}`
   - `{{ cnpj_empresa }}`
   - `{{ periodo_anual }}`
   - `{{ socios }}` — lista de dicionários
   - `{{ balanco_patrimonial_pt1 }}` — imagem inline
   - `{{ data_atual }}`

**Referência:** [docxtpl documentation](https://docxtpl.readthedocs.io/)

### Variáveis de Ambiente

Edite `config/settings.py` para adicionar novas variáveis:

```python
# Exemplo: adicionar timeout de requisição
REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", "30"))
```

Depois, no seu código:
```python
from config import REQUEST_TIMEOUT
response = requests.post(..., timeout=REQUEST_TIMEOUT)
```

### Integração n8n

O webhook n8n recebe:

**Metadados (form-data):**
```json
{
  "nome_empresa": "Empresa XYZ",
  "razao_social_empresa": "Empresa XYZ Ltda",
  "cnpj_empresa": "00.000.000/0001-00",
  "periodo_anual": "Janeiro a Dezembro de 2024",
  "periodo_em_data": "01 a 12/24",
  "data_dem_encerradas": "31/12/2024",
  "socios": "[{\"nome\": \"Sócio 1\", \"cpf\": \"000.000.000-00\", \"cargo\": \"Diretor\"}]"
}
```

**Arquivo:**
```
arquivo_dossie: (binary DOCX)
```

Configure em `config/settings.py`:
```python
N8N_WEBHOOK_URL = "https://seu-dominio.com/webhook/..."
N8N_ENABLED = True  # ou variável de ambiente
```

---

## 📋 Checklist para Deploy

Antes de fazer deploy (Streamlit Cloud, Docker, servidor próprio):

- [ ] Testar localmente: `streamlit run main.py`
- [ ] Executar suite de testes: `pytest`
- [ ] Verificar `requirements.txt` atualizado: `pip freeze > requirements.txt`
- [ ] Confirmar que `template_base_ofc.docx` está no repositório
- [ ] Testar com valores reais (CNPJ, CPF válidos)
- [ ] Validar integração n8n se habilitada
- [ ] Revisar logs: `tail -f logs/app.log`
- [ ] Documentar mudanças no CHANGELOG

---

## 🐛 Troubleshooting

### "Template not found: template_base_ofc.docx"

**Causa:** Arquivo template está faltando no repositório ou no diretório de trabalho.

**Solução:**
```bash
# Verifique se o arquivo existe
ls -la template_base_ofc.docx

# Se em um subdirectory, atualize config/settings.py:
TEMPLATE_PATH = BASE_DIR / "caminho" / "template_base_ofc.docx"
```

### "No pandoc was found"

**Causa:** Pandoc não foi instalado.

**Solução:** Veja [Instalação do Pandoc](#instalação-do-pandoc)

### "PDF must have at least 2 pages"

**Causa:** Balanço Patrimonial tem menos de 2 páginas.

**Solução:** Verifique o PDF. Muitas vezes é necessário dividir em 2 PDFs e enviar ambos como "Balanço Patrimonial".

### "Placeholder not found in document"

**Causa:** O template DOCX foi modificado e um placeholder foi deletado acidentalmente.

**Solução:**
1. Abra `template_base_ofc.docx` no Word
2. Verifique se contém: `[[DEMONSTR_RESULTADO]]`, `[[EXP_DEMONSTR]]`, `[[CARTA_RESP]]`
3. Se faltarem, insira novamente nos locais corretos

### Erro de conexão n8n (timeout)

**Verificar:**
```bash
# Teste a URL manualmente
curl -X POST https://seu-n8n.com/webhook/... \
  -F "nome_empresa=Teste" \
  -F "arquivo_dossie=@exemplo.docx"

# Se retornar 200, o problema é a configuração no Streamlit
```

---

## 📚 Stack Tecnológico

| Biblioteca | Versão | Uso |
|-----------|--------|-----|
| **Streamlit** | 1.28+ | Interface web |
| **docxtpl** | 0.16+ | Template DOCX com Jinja2 |
| **python-docx** | 0.8.11+ | Manipulação DOCX |
| **PyMuPDF (fitz)** | 1.23+ | Conversão PDF → PNG |
| **loguru** | 0.7+ | Logging estruturado |
| **requests** | 2.31+ | Requisições HTTP (n8n) |
| **pytest** | 7.4+ | Testes unitários |

---

## 🤝 Contribuindo

1. **Fork** o repositório
2. Crie uma **branch** para sua feature: `git checkout -b feat/minha-feature`
3. **Commit** as mudanças: `git commit -m "Adiciona minha feature"`
4. **Push** para a branch: `git push origin feat/minha-feature`
5. Abra um **Pull Request**

### Padrões de código

- **Formatação:** Black (`black app/ config/ tests/`)
- **Linting:** Ruff (`ruff check app/ config/ tests/`)
- **Type hints:** Fortemente recomendado
- **Docstrings:** Google-style (`"""Descrição. Args: Returns:"""`)

```bash
# Formatar automaticamente
black app/ config/ tests/
ruff check --fix app/ config/ tests/
```

---

## 📝 Changelog

### v1.1.0 — Refatoração Profissional (Current)

✅ Estrutura modular completa (core, utils, config)
✅ Classe `DossieAutomation` para orquestração
✅ Classe `FileProcessor` para processamento de PDFs/DOCXs
✅ Helpers centralizados (formatação, validação)
✅ Logging com loguru
✅ Suite de testes (pytest)
✅ Documentação extensiva

### v1.0.0 — Inicial

- Gerador básico em `app_gerador.py`
- Interface Streamlit
- Integração n8n

---

## 📄 Licença

Este projeto está sob licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 📞 Suporte

- **Issues:** [GitHub Issues](https://github.com/camposs04/Automatizar_Dossie/issues)
- **Email:** [seu-email-aqui]

---

## ✨ Agradecimentos

- Contribuidores do projeto
- Comunidade Streamlit
- [docxtpl](https://docxtpl.readthedocs.io/) — renderização elegante de templates
- [PyMuPDF](https://pymupdf.readthedocs.io/) — processamento eficiente de PDFs

---

**Desenvolvido com ❤️ em Brasília, Brasil**
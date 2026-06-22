# 🤝 Guia de Contribuição

Obrigado por querer contribuir com o **Automatizar Dossiê**! Este documento explica como fazer isso de forma eficaz.

---

## 📋 Código de Conduta

Esperamos que todos os contribuidores:

- Sejam respeitosos e inclusivos
- Forneçam feedback construtivo
- Focados em melhorar o projeto
- Evitem linguagem ofensiva ou discriminatória

---

## 🚀 Como Contribuir

### 1. Reportar um Bug

**Abra uma issue** descrevendo:

- Título claro: `[BUG] Descrição do problema`
- Passo a passo para reproduzir
- Comportamento esperado vs. observado
- Ambiente (Python, SO, versão Streamlit)
- Logs (se houver)

**Template:**

```markdown
## Descrição do Bug
Descreva o problema brevemente.

## Passos para Reproduzir
1. Faça isso
2. Depois aquilo
3. O erro ocorre

## Comportamento Esperado
Deveria fazer X, mas fez Y.

## Environment
- Python: 3.10
- SO: Linux / macOS / Windows
- Versão Streamlit: 1.28
- Stack trace: [colar aqui]
```

### 2. Sugerir uma Feature

**Abra uma issue** com:

- Título: `[FEATURE] Nome da feature`
- Descrição clara do caso de uso
- Benefício esperado
- Exemplos ou mockups (se aplicável)

### 3. Submeter um Pull Request (PR)

#### Pré-requisitos

- Fork o repositório
- Clone localmente: `git clone https://github.com/seu-usuario/Automatizar_Dossie.git`
- Crie uma branch: `git checkout -b feat/minha-feature` ou `bugfix/meu-bug`

#### Desenvolvimento

1. **Instale dependências de desenvolvimento:**
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

2. **Faça suas mudanças** seguindo os padrões do projeto

3. **Escreva testes** para sua funcionalidade:
   ```bash
   pytest tests/ -v
   ```

4. **Formate o código:**
   ```bash
   black app/ config/ tests/
   ruff check --fix app/ config/ tests/
   ```

5. **Verifique a cobertura:**
   ```bash
   pytest --cov=app tests/
   ```

6. **Commit com mensagem descritiva:**
   ```bash
   git commit -m "feat(core): adiciona suporte a XLS no balanço"
   git commit -m "fix(utils): corrige formatação de CNPJ com 13 dígitos"
   git commit -m "docs(readme): atualiza instruções de instalação"
   ```

7. **Push e abra um PR:**
   ```bash
   git push origin feat/minha-feature
   ```

---

## 📐 Padrões de Código

### Estrutura de Diretórios

```
app/
├── core/              # Lógica de negócio
├── utils/             # Helpers e utilitários
├── main.py            # Interface (Streamlit)
└── __init__.py

config/
├── settings.py        # Configurações (env vars)
├── constants.py       # Constantes estáticas
└── __init__.py

tests/
├── test_core.py
├── test_utils.py
└── __init__.py
```

### Convenções de Código

#### Nomes

- **Funções/variáveis:** `snake_case`
- **Classes:** `PascalCase`
- **Constantes:** `SCREAMING_SNAKE_CASE`

```python
# ✅ Correto
def format_cnpj(cnpj: str) -> str:
    pass

class FileProcessor:
    pass

MAX_UPLOAD_SIZE = 50 * 1024 * 1024
```

#### Type Hints

Sempre use type hints:

```python
# ✅ Bom
def save_upload_to_temp(uploaded_file: UploadedFile) -> str:
    """Salva upload em arquivo temporário."""
    ...

def insert_pdf_at_placeholder(
    main_doc: Document,
    placeholder: str,
    pdf_path: str
) -> bool:
    """Substitui placeholder por imagens do PDF."""
    ...
```

#### Docstrings

Use Google-style docstrings:

```python
def build_periodo_anual(data_inicio, data_fim) -> str:
    """
    Gera descrição longa do período contábil.
    
    Exemplo: 'Janeiro a Dezembro de 2024'.
    
    Args:
        data_inicio: Data de início (datetime.date).
        data_fim: Data de fim (datetime.date).
    
    Returns:
        String descritiva do período.
    
    Raises:
        ValueError: Se data_fim < data_inicio.
    """
    ...
```

#### Tamanho de Linhas

- Máximo: **100 caracteres** (Black + Ruff)
- Quebras automáticas com Black

```python
# ✅ Bom (formatado por Black)
result = automation.send_to_n8n(
    input_data=data,
    file_bytes=file_content,
    timeout=30
)
```

#### Imports

Organize assim:

```python
# 1. Standard library
import datetime
import os
from pathlib import Path

# 2. Third-party
import streamlit as st
from docx import Document

# 3. Local
from app.core.automation import DossieAutomation
from config.settings import TEMPLATE_PATH
```

### Logging

Use `loguru` para logs:

```python
from app.utils.logger import logger

logger.info(f"Dossiê gerado para {empresa}.")
logger.warning(f"Placeholder '{key}' não encontrado.")
logger.error(f"Erro ao processar PDF: {exc}")
logger.debug(f"Variável temporária: {temp_var}")
```

**Nunca use `print()`** — use logger para produção.

---

## 🧪 Testes

### Escrever Testes

Use **pytest**. Exemplo:

```python
# tests/test_file_processor.py

import pytest
from app.core.file_processor import FileProcessor

class TestFileProcessor:
    @pytest.fixture
    def processor(self):
        return FileProcessor()
    
    def test_validate_file_docx(self, processor):
        assert processor.validate_file("doc.docx") is True
    
    def test_validate_file_invalid(self, processor):
        assert processor.validate_file("doc.xls") is False
```

### Coverage

Mire por **>80% de cobertura**:

```bash
pytest --cov=app --cov-report=term-missing
```

### Executar Testes Localmente

```bash
# Todos os testes
pytest

# Com verbosidade
pytest -v

# Teste específico
pytest tests/test_file_processor.py::TestFileProcessor::test_validate_file_docx

# Com cobertura
pytest --cov=app --cov-report=html
# Abra: htmlcov/index.html
```

---

## 📝 Mensagens de Commit

Siga [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>(<escopo>): <descrição curta>

<corpo (opcional)>

<rodapé (opcional)>
```

### Tipos

- **feat:** Nova feature
- **fix:** Correção de bug
- **docs:** Documentação
- **refactor:** Refatoração sem mudança funcional
- **test:** Adição de testes
- **chore:** Mudanças de build, deps, config

### Exemplos

```bash
git commit -m "feat(core): adiciona suporte a XLS no balanço"
git commit -m "fix(utils): corrige formatação de CNPJ"
git commit -m "docs(readme): atualiza instruções"
git commit -m "refactor(automation): simplifica lógica de renderização"
git commit -m "test(file-processor): adiciona testes para pdf_to_images"
```

---

## 🔄 Processo de Review

1. **GitHub Actions** roda testes automaticamente
2. Manutenedor revisa código (1-3 dias)
3. Solicitaremos mudanças se necessário
4. Após aprovação, seu PR é merged

### Checklist de Review

- [ ] Código segue padrões do projeto?
- [ ] Testes cobrem a mudança?
- [ ] Docstring está presente?
- [ ] Sem `print()` ou `TODO` esquecidos?
- [ ] CHANGELOG foi atualizado?

---

## 📚 Estrutura de uma Feature Completa

Se estiver adicionando algo novo, siga este checklist:

### 1. Código

```
✅ Arquivo principal em app/core/ ou app/utils/
✅ Type hints completos
✅ Docstrings Google-style
✅ Logging apropriado
```

### 2. Testes

```
✅ Arquivo de teste em tests/
✅ Cobertura > 80%
✅ Casos de sucesso + erro
```

### 3. Integração

```
✅ app/main.py atualizado (se UI)
✅ config/* atualizado (se novas config/constantes)
```

### 4. Documentação

```
✅ Docstring na função/classe
✅ README.md atualizado (se feature maior)
✅ CHANGELOG.md atualizado
```

### 5. Exemplo completo: Adicionar validação de CPF

**1. `app/utils/helpers.py`:**
```python
def validate_cpf(cpf: str) -> bool:
    """Valida CPF usando algoritmo oficial."""
    cpf = clean_numbers(cpf)
    if len(cpf) != 11:
        return False
    # ... validação
    return True
```

**2. `tests/test_helpers.py`:**
```python
def test_validate_cpf_valid():
    assert validate_cpf("123.456.789-00") is True

def test_validate_cpf_invalid():
    assert validate_cpf("000.000.000-00") is False
```

**3. `app/main.py`:**
```python
from app.utils.helpers import validate_cpf

cpf_input = st.text_input("CPF")
if cpf_input and not validate_cpf(cpf_input):
    st.error("CPF inválido!")
```

**4. `README.md`** — documente a mudança na seção apropriada.

---

## 🚨 Grandes Mudanças

Se sua contribuição é **estrutural** (muda arquitetura, renomeia módulos, etc.):

1. **Abra uma issue** para discussão **antes** de começar
2. Descreva a motivação e impacto
3. Aguarde feedback dos manutenedores
4. Proceda após aprovação

---

## 📞 Dúvidas?

- **Issues:** GitHub Issues
- **Discussões:** GitHub Discussions
- **Email:** [contato@seu-dominio.com]

---

## ✨ Agradecimentos

Agradecemos por contribuir! Seus esforços melhoram o projeto para todos.

**Happy coding! 🎉**
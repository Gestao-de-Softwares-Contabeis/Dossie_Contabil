# 📦 Guia Completo de Instalação

Instruções passo-a-passo para instalar e configurar o projeto em seu ambiente.

---

## 📋 Pré-requisitos

### Sistema Operacional
- **Linux:** Ubuntu 20.04+, Debian 11+, ou similar
- **macOS:** 10.15+ (Intel ou Apple Silicon)
- **Windows:** 10 ou 11 (PowerShell ou cmd.exe)

### Requisitos Obrigatórios

#### Python 3.10 ou superior

**Verificar versão:**
```bash
python --version
# Deve retornar: Python 3.10.x ou superior
```

**Instalar Python:**

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3.10 python3.10-venv python3-pip
```

**macOS (Homebrew):**
```bash
brew install python@3.10
```

**Windows:**
- Baixe em: [python.org](https://www.python.org/downloads/)
- Marque: "Add Python to PATH" durante instalação

#### Pandoc (necessário para Markdown → DOCX)

**Linux:**
```bash
sudo apt-get update
sudo apt-get install pandoc
# Verificar: pandoc --version
```

**macOS:**
```bash
brew install pandoc
# Verificar: pandoc --version
```

**Windows:**
- Opção 1: [pandoc.org/installing.html](https://pandoc.org/installing.html)
- Opção 2: `choco install pandoc` (Chocolatey)

---

## 🚀 Instalação Passo-a-Passo

### Passo 1: Clonar o Repositório

```bash
# Clone
git clone https://github.com/camposs04/Automatizar_Dossie.git

# Entre no diretório
cd Automatizar_Dossie
```

Ou se preferir, **baixe o ZIP** do GitHub e descompacte.

### Passo 2: Criar Ambiente Virtual

Um ambiente virtual isola dependências Python deste projeto.

**Linux/macOS:**
```bash
python3.10 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**Windows (cmd.exe):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Verificar ativação:**
```bash
# Seu prompt deve começar com: (venv)
which python  # Linux/macOS
# ou
where python  # Windows
```

### Passo 3: Atualizar pip

```bash
pip install --upgrade pip
```

### Passo 4: Instalar Dependências

```bash
pip install -r requirements.txt
```

**O que será instalado:**
- streamlit (interface)
- docxtpl (templates DOCX)
- python-docx (manipulação DOCX)
- PyMuPDF (conversão PDF)
- loguru (logging)
- requests (HTTP para n8n)
- pytest (testes)
- black, ruff (formatação de código)

**Tempo esperado:** 2-5 minutos (depende de internet)

### Passo 5: Configurar Variáveis de Ambiente (Opcional)

Se quiser usar n8n ou customizar parâmetros:

```bash
# Copie o template
cp .env.example .env

# Edite com seus valores
nano .env  # Linux/macOS
# ou
notepad .env  # Windows
```

**Variáveis importantes:**
```env
N8N_WEBHOOK_URL=https://seu-dominio-n8n.com/webhook/...
N8N_ENABLED=true
PDF_DPI=200
LOG_LEVEL=INFO
```

Se não configurar, valores padrão serão usados.

### Passo 6: Verificar Instalação

```bash
# Teste se tudo está funcionando
python -c "import streamlit; print(f'Streamlit {streamlit.__version__} OK')"
python -c "import docxtpl; print('docxtpl OK')"
python -c "import fitz; print('PyMuPDF OK')"
python -c "import pandoc; print('pandoc OK')"

# Se tudo imprimir "OK", você está pronto!
```

---

## ▶️ Executar a Aplicação

### Modo Normal

```bash
streamlit run main.py
```

A aplicação abrirá em: **http://localhost:8501**

### Com Debug

```bash
# Mais verboso
LOG_LEVEL=DEBUG streamlit run main.py
```

### Detalhes de Execução

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://xxx.xxx.xxx.xxx:8501

  For better performance, install the Streamlit HTTP server again.
  To stop the server, press Ctrl + C.
```

---

## 🧪 Executar Testes

### Todos os testes

```bash
pytest tests/ -v
```

### Com cobertura de código

```bash
pytest --cov=app tests/ --cov-report=html
# Abre relatório em: htmlcov/index.html
```

### Teste específico

```bash
pytest tests/test_file_processor.py::TestFileProcessor::test_validate_file_docx -v
```

---

## 📚 Instalação com Make (Opcional)

Se tem `make` instalado:

```bash
# Ver tarefas disponíveis
make help

# Instalar dependências
make install

# Instalar com dev tools
make dev

# Rodar aplicação
make run

# Executar testes
make test

# Formatar código
make format
```

---

## 🐳 Docker (Opcional)

Se preferir containerizar:

### Opção 1: VS Code Dev Container

1. Abra o projeto no VS Code
2. Pressione `Ctrl+Shift+P` → "Dev Container: Reopen in Container"
3. Aguarde setup (2-5 minutos)
4. Pronto! Environment pronto automaticamente

### Opção 2: Docker Manual

```dockerfile
FROM python:3.10-slim

RUN apt-get update && apt-get install -y pandoc

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["streamlit", "run", "main.py", "--server.port=8501"]
```

Depois:
```bash
docker build -t automatizar-dossie .
docker run -p 8501:8501 automatizar-dossie
```

---

## ☁️ Deploy em Streamlit Cloud

1. Faça **push** para GitHub
2. Vá para [streamlit.io/cloud](https://streamlit.io/cloud)
3. Clique em **"New app"**
4. Selecione seu repositório
5. Branch: `main`
6. Main file path: `main.py`
7. Clique **"Deploy!"**

**Configurar secrets:**
- Vá para **Settings** → **Secrets**
- Cole o conteúdo de `.env` (sem comentários)

---

## 🔧 Troubleshooting

### ❌ "Python: command not found"

**Solução:**
```bash
python3 --version  # Tente python3
python3 -m venv venv
```

Ou instale Python conforme [Pré-requisitos](#python-310-ou-superior).

### ❌ "No module named 'streamlit'"

**Solução:**
```bash
# Verify venv is activated
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows

# Reinstall
pip install --upgrade pip
pip install -r requirements.txt
```

### ❌ "pandoc: command not found"

**Solução:** Instale Pandoc conforme [Pré-requisitos](#pandoc-necessário-para-markdown--docx).

### ❌ "template_base_ofc.docx not found"

**Solução:** O arquivo template precisa estar no repositório GitHub ou ser criado manualmente. Verifique se está na raiz do projeto.

### ❌ Porta 8501 já está em uso

**Solução:**
```bash
streamlit run main.py --server.port=8502
# Ou libere a porta:
lsof -i :8501  # Linux/macOS
netstat -ano | findstr :8501  # Windows
```

### ❌ "pip: command not found"

**Solução:**
```bash
python -m pip --version
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## ✅ Verificação Final

Você sabe que está pronto quando:

- [ ] `python --version` retorna 3.10+
- [ ] `pandoc --version` funciona
- [ ] `(venv)` aparece no seu prompt
- [ ] `pip list` mostra streamlit, docxtpl, etc
- [ ] `streamlit run main.py` abre navegador
- [ ] Interface carrega sem erros
- [ ] `pytest tests/` passa com sucesso

---

## 📞 Próximos Passos

1. Leia `QUICKSTART.md` para começar rapidinho
2. Leia `README.md` para visão geral completa
3. Leia `DEVELOPMENT.md` se vai modificar código

---

**Instalação concluída! Vamos ao trabalho! 🚀**
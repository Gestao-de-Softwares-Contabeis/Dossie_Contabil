# Automatizar Dossiê Contábil

Sistema que automatiza a geração de dossiês contábeis em DOCX a partir de balanços em PDF, notas explicativas e dados da empresa/sócios. Possui interface web em Streamlit e integração opcional com n8n para envio automático do documento gerado.

## Tecnologias

- Python 3.10+
- Streamlit
- docxtpl / python-docx
- PyMuPDF
- pypandoc
- requests (integração n8n)
- loguru
- pytest

## Pré-requisitos

- Python 3.10+
- pip
- Pandoc
- Git

## Instalação e Execução

```bash
git clone https://github.com/camposs04/Automatizar_Dossie.git
cd Dossie_Contabil/outputs/Automatizar_Dossie
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```bash
streamlit run main.py
```

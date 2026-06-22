# 🔧 Guia Técnico de Desenvolvimento
 
Este documento detalha como **modificar e estender** o projeto de forma profissional.
 
---
 
## 📋 Índice
 
1. [Adicionando novas funcionalidades](#-adicionando-novas-funcionalidades)
2. [Modificando o template DOCX](#-modificando-o-template-docx)
3. [Alterando configurações](#-alterando-configurações)
4. [Estendendo validações](#-estendendo-validações)
5. [Integrações externas](#-integrações-externas)
6. [Debugging e logging](#-debugging-e-logging)
---
 
## 🚀 Adicionando Novas Funcionalidades
 
### Exemplo 1: Suporte a Planilha XLS no Balanço
 
Você quer permitir que usuários façam upload de balanços em Excel (XLS/XLSX) além de PDF.
 
#### 1. Atualize `config/constants.py`
 
```python
UPLOAD_KEYS = {
    "balanco": "balanco_file",              # PDF
    "balanco_xls": "balanco_xls_file",      # ← NOVO
    "dre": "demstr_result_file",
    "notas": "explic_demonstr_file",
    "carta": "carta_responsb_file",
}
```
 
#### 2. Estenda `app/core/file_processor.py`
 
```python
import openpyxl
from PIL import Image
import io
 
class FileProcessor:
    
    def xls_to_images(self, xls_path: str) -> list[bytes]:
        """
        Converte primeira página de planilha Excel em imagem PNG.
        
        Usa: openpyxl (ler sheet) + PIL (renderizar como imagem).
        
        Args:
            xls_path: Caminho do arquivo .xls ou .xlsx
            
        Returns:
            Lista com 1 imagem PNG (bytes) por página renderizada.
            
        Raises:
            ValueError: Se arquivo estiver vazio ou sem dados.
        """
        try:
            # Abre a planilha
            wb = openpyxl.load_workbook(xls_path)
            ws = wb.active
            
            # Renderiza como imagem (simplificado)
            # Em produção, use biblioteca como "openpyxl-image-loader"
            # ou converta para PDF primeiro, depois para PNG
            
            logger.info(f"Planilha '{xls_path}' convertida para imagem.")
            # Retorna bytes PNG (aqui simplificado)
            return [b"fake_png_bytes"]
        except Exception as exc:
            logger.error(f"Erro ao converter XLS: {exc}")
            raise ValueError(f"Não foi possível processar XLS: {exc}")
```
 
**Dependência obrigatória:** Atualize `requirements.txt`
 
```
openpyxl>=3.1.0
Pillow>=10.0.0  # Para renderização de imagem
```
 
#### 3. Atualize `app/core/automation.py`
 
```python
from config.constants import UPLOAD_KEYS
 
class DossieAutomation:
    
    def _render_template(self, input_data: dict, temp_paths: dict) -> str:
        """Renderiza o template DOCX com dados."""
        doc = DocxTemplate(str(TEMPLATE_PATH))
        
        # ← NOVO: Detectar se é PDF ou XLS
        balanco_key = UPLOAD_KEYS["balanco"]  # "balanco_file"
        balanco_xls_key = UPLOAD_KEYS["balanco_xls"]  # "balanco_xls_file"
        
        if balanco_xls_key in temp_paths:
            # Usuário enviou XLS
            balanco_bytes = self._processor.xls_to_images(temp_paths[balanco_xls_key])[0]
            balanco_img = InlineImage(doc, BytesIO(balanco_bytes), width=Inches(6))
        else:
            # Usuário enviou PDF (padrão)
            pt1_bytes, pt2_bytes = self._processor.pdf_balanco_duas_paginas(
                temp_paths[balanco_key]
            )
            balanco_img = InlineImage(doc, BytesIO(pt1_bytes), width=Inches(6))
            # ... pt2 também
        
        context = {
            # ... outros campos
            "balanco_patrimonial_pt1": balanco_img,
            # ...
        }
        # ...
```
 
#### 4. Atualize `app/main.py`
 
```python
with col5:
    # Original
    input_data["uploads"]["balanco_file"] = st.file_uploader(
        "Balanço Patrimonial (PDF)", type=["pdf"]
    )
    
    # ← NOVO: opção XLS
    with st.expander("Ou use XLS/XLSX", expanded=False):
        input_data["uploads"]["balanco_xls_file"] = st.file_uploader(
            "Balanço Patrimonial (Excel)", type=["xls", "xlsx"]
        )
 
# Validação: exigir um dos dois
required = [
    ("balanco_file", "Balanço (PDF)"),
    ("demstr_result_file", "DRE (PDF)"),
    ("explic_demonstr_file", "Notas (DOCX)"),
    ("carta_responsb_file", "Carta (DOCX)"),
]
 
# Balanço: ou PDF ou XLS
has_balanco = input_data["uploads"].get("balanco_file") or input_data["uploads"].get("balanco_xls_file")
 
if not has_balanco:
    st.warning("Envie o Balanço em PDF ou XLS")
```
 
#### 5. Escreva testes em `tests/test_file_processor.py`
 
```python
def test_xls_to_images_valid_file(self, processor, tmp_path):
    """Testa conversão de XLS válido para imagens."""
    # Mock de um arquivo XLS válido
    xls_path = tmp_path / "teste.xlsx"
    
    # (Criar arquivo XLS com openpyxl)
    # images = processor.xls_to_images(str(xls_path))
    # assert len(images) >= 1
    # assert isinstance(images[0], bytes)
 
def test_xls_to_images_raises_on_empty(self, processor):
    """Testa se erro é lançado para XLS vazio."""
    with pytest.raises(ValueError, match="vazio"):
        processor.xls_to_images("/path/to/empty.xlsx")
```
 
#### 6. Atualize documentação
 
**README.md:**
```markdown
| **Balanço Patrimonial** | PDF ou XLSX | 2 páginas se PDF; qualquer tamanho se Excel |
```
 
**CHANGELOG.md:**
```markdown
## [Unreleased]
 
### Added
- ✨ Suporte para upload de Balanço em Excel (XLS/XLSX)
```
 
**`config/constants.py` (docstring):**
```python
"""
Constantes estáticas da aplicação.
 
Balanços aceitos:
- PDF: 2 páginas (pt1 + pt2)
- XLSX: conversão automática para imagem
"""
```
 
---
 
## 📝 Modificando o Template DOCX
 
O template `template_base_ofc.docx` usa **Jinja2** para renderização dinâmica.
 
### Variáveis Disponíveis
 
Em `app/core/automation.py`, o contexto inclui:
 
```python
context = {
    # Dados da empresa
    "nome_empresa": str,
    "razao_social_empresa": str,
    "cnpj_empresa": str,
    
    # Período
    "periodo_anual": str,              # Ex: "Janeiro a Dezembro de 2024"
    "periodo_em_data": str,            # Ex: "01 a 12/24"
    "data_dem_encerradas": str,        # Ex: "31/12/2024"
    
    # Documentos
    "balanco_patrimonial_pt1": InlineImage,
    "balanco_patrimonial_pt2": InlineImage,
    
    # Sócios
    "socios": [
        {"nome": str, "cpf": str, "cargo": str},
        ...
    ],
    
    # Placeholders a serem substituídos depois
    "demontr_resultado": str,          # [[DEMONSTR_RESULTADO]]
    "explic_demonstr": str,            # [[EXP_DEMONSTR]]
    "carta_responsb": str,             # [[CARTA_RESP]]
    
    # Data de geração
    "data_atual": str,                 # Ex: "19 de Junho de 2024"
}
```
 
### Editando o Template
 
1. **Abra no Word:**
```bash
   open template_base_ofc.docx  # macOS
   # ou
   start template_base_ofc.docx  # Windows
```
 
2. **Insira variáveis com Jinja2:**
```docx
   Empresa: {{ nome_empresa }}
   Razão Social: {{ razao_social_empresa }}
   CNPJ: {{ cnpj_empresa }}
```
 
3. **Loops para sócios:**
```docx
   {% for socio in socios %}
   Sócio: {{ socio.nome }}
   CPF: {{ socio.cpf }}
   Cargo: {{ socio.cargo }}
   {% endfor %}
```
 
4. **Inserir imagens:**
   Insira um espaço reservado (placeholder):
```docx
   [IMAGEM DO BALANÇO AQUI]
```
   
   Depois, no código:
```python
   context["balanco_patrimonial_pt1"] = InlineImage(doc, BytesIO(img), width=Inches(6))
```
 
5. **Placeholders para conteúdo dinâmico (DOCX/Markdown):**
```docx
   [[DEMONSTR_RESULTADO]]
   [[EXP_DEMONSTR]]
   [[CARTA_RESP]]
```
 
### Validar Edições
 
```bash
# Teste local
streamlit run main.py
 
# Envie um formulário de teste
# Verifique o DOCX gerado
```
 
---
 
## ⚙️ Alterando Configurações
 
### Variáveis de Ambiente
 
Crie `.env` na raiz:
 
```env
# n8n
N8N_WEBHOOK_URL=https://seu-dominio-n8n.com/webhook/receber-dados
N8N_ENABLED=true
 
# PDF
PDF_DPI=200
IMAGE_WIDTH_INCHES=6
 
# Logging
LOG_LEVEL=DEBUG
```
 
Use em `config/settings.py`:
 
```python
import os
 
N8N_WEBHOOK_URL = os.environ.get("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/...")
PDF_DPI = int(os.environ.get("PDF_DPI", "200"))
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
```
 
### Constantes Globais
 
Edite `config/constants.py`:
 
```python
# Meses em português
MESES_PT = {
    1: "Janeiro",
    # ... adicione mais conforme necessário
}
 
# Placeholders do template
PLACEHOLDER_DRE = "[[DEMONSTR_RESULTADO]]"
 
# Tamanho máximo de upload (bytes)
MAX_UPLOAD_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB
```
 
---
 
## ✅ Estendendo Validações
 
### Adicione validação de CPF
 
Em `app/utils/helpers.py`:
 
```python
def validate_cpf(cpf: str) -> bool:
    """
    Valida CPF usando algoritmo oficial (módulo 11).
    
    Retorna False se:
    - Tem menos de 11 dígitos
    - Todos os dígitos são iguais (ex: 111.111.111-11)
    - Dígitos verificadores estão incorretos
    """
    cpf = clean_numbers(cpf)
    
    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False
    
    def calc_digit(cpf_seq, factor):
        total = sum(int(d) * f for d, f in zip(cpf_seq, range(factor, 1, -1)))
        remainder = (total * 10) % 11
        return remainder if remainder < 10 else 0
    
    d1 = calc_digit(cpf[:9], 10)
    d2 = calc_digit(cpf[:10], 11)
    
    return int(cpf[9]) == d1 and int(cpf[10]) == d2
```
 
Use em `app/main.py`:
 
```python
from app.utils.helpers import validate_cpf
 
cpf_raw = st.text_input(f"CPF do Sócio {i+1}")
 
if cpf_raw and not validate_cpf(cpf_raw):
    st.error("❌ CPF inválido")
    st.stop()
 
st.session_state.socios[i]["cpf"] = format_cpf(cpf_raw)
```
 
---
 
## 🔗 Integrações Externas
 
### Webhook n8n
 
Configurado em `app/core/automation.py`:
 
```python
def send_to_n8n(self, input_data: dict, file_bytes: bytes) -> tuple[bool, str]:
    """Envia dossiê para webhook n8n."""
    # Já implementado — customize conforme necessário
```
 
**Dados enviados:**
 
```json
{
  "nome_empresa": "XYZ Ltda",
  "razao_social_empresa": "XYZ Empresa Ltda",
  "cnpj_empresa": "00.000.000/0001-00",
  "periodo_anual": "Janeiro a Dezembro de 2024",
  "socios": "[{\"nome\": \"João\", \"cpf\": \"000.000.000-00\", \"cargo\": \"Diretor\"}]",
  "arquivo_dossie": <binary DOCX>
}
```
 
### Adicionar Integração com Banco de Dados
 
Exemplo: Salvar metadados em PostgreSQL após geração.
 
1. **Instale driver:**
```bash
   pip install psycopg2-binary
```
 
2. **Atualize `app/core/automation.py`:**
```python
   import psycopg2
   
   def save_to_database(self, input_data: dict) -> bool:
       """Salva metadados em PostgreSQL."""
       try:
           conn = psycopg2.connect(
               host=os.environ["DB_HOST"],
               database=os.environ["DB_NAME"],
               user=os.environ["DB_USER"],
               password=os.environ["DB_PASS"]
           )
           cursor = conn.cursor()
           cursor.execute(
               "INSERT INTO dossies (nome_empresa, cnpj, data_criacao) VALUES (%s, %s, %s)",
               (input_data["nome_empresa"], input_data["cnpj_empresa"], datetime.datetime.now())
           )
           conn.commit()
           cursor.close()
           conn.close()
           logger.info(f"Salvo em DB: {input_data['nome_empresa']}")
           return True
       except Exception as exc:
           logger.error(f"Erro ao salvar em DB: {exc}")
           return False
```
 
3. **Chame em `generate()`:**
```python
   self.save_to_database(input_data)
```
 
---
 
## 🐛 Debugging e Logging
 
### Ativar Modo Debug
 
Em `app/utils/logger.py`:
 
```python
# Mude de "INFO" para "DEBUG"
logger.add(
    sys.stderr,
    level="DEBUG",  # ← Mais verboso
    format="..."
)
```
 
Ou via variável:
 
```python
import os
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
logger.add(sys.stderr, level=LOG_LEVEL, ...)
```
 
### Log de Variáveis
 
```python
from app.utils.logger import logger
 
logger.debug(f"Input: {input_data}")
logger.info(f"Processando {empresa}")
logger.warning(f"CNPJ suspeito: {cnpj}")
logger.error(f"Falha ao processar: {exc}")
```
 
### Inspeção em Tempo Real (Streamlit)
 
```python
st.write("Debug — input_data:")
st.json(input_data)
 
st.write("Debug — temp_paths:")
st.json(temp_paths)
```
 
### Breakpoints com pdb
 
```python
import pdb
 
def minha_funcao(data):
    pdb.set_trace()  # Para aqui quando rodar
    # ...
```
 
Depois:
```bash
python -c "from app.core.automation import DossieAutomation; ..."
```
 
---
 
## 📊 Monitoramento
 
### Health Check
 
Adicione endpoint de saúde:
 
```python
# app/main.py
if st.sidebar.checkbox("🔧 Admin"):
    st.write("### Health Check")
    st.write(f"Template exists: {TEMPLATE_PATH.exists()}")
    st.write(f"Log level: {os.environ.get('LOG_LEVEL', 'INFO')}")
    st.write(f"n8n enabled: {N8N_ENABLED}")
```
 
### Métricas
 
Conte gerados com sucesso:
 
```python
# Em app/core/automation.py
import json
from pathlib import Path
 
METRICS_FILE = Path("metrics.json")
 
def record_success(input_data):
    """Registra dossiê gerado com sucesso."""
    metrics = json.loads(METRICS_FILE.read_text()) if METRICS_FILE.exists() else {}
    
    key = input_data["nome_empresa"]
    metrics[key] = {
        "timestamp": datetime.datetime.now().isoformat(),
        "cnpj": input_data["cnpj_empresa"]
    }
    
    METRICS_FILE.write_text(json.dumps(metrics, indent=2))
```
 
---
 
## 🎯 Próximos Passos
 
- [ ] Adicionar suporte a múltiplos idiomas (i18n)
- [ ] Exportar para PDF além de DOCX
- [ ] Autenticação de usuários
- [ ] Dashboard de histórico de dossiês
- [ ] Assinatura digital automática
---
 
**Happy developing! 🚀**
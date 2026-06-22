"""
Configurações centralizadas da aplicação.
Edite este arquivo para ajustar caminhos, limites e integrações.
"""
import os
from pathlib import Path

# Raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Caminhos principais
TEMPLATE_PATH = BASE_DIR / "template_base_ofc.docx"
TEMP_DIR = Path(os.environ.get("TEMP_DIR", "/tmp"))

# Integração n8n
N8N_WEBHOOK_URL = os.environ.get(
    "N8N_WEBHOOK_URL",
    "https://genai.up4me.io/webhook-test/receber-dados"
)
N8N_ENABLED = os.environ.get("N8N_ENABLED", "true").lower() == "true"

# Configurações de imagem (DPI para conversão PDF → PNG)
PDF_DPI = int(os.environ.get("PDF_DPI", "200"))
IMAGE_WIDTH_INCHES = float(os.environ.get("IMAGE_WIDTH_INCHES", "6"))

# Tamanho máximo de upload (bytes) — 50 MB
MAX_UPLOAD_SIZE_BYTES = 50 * 1024 * 1024

# Uploads aceitos
ALLOWED_IMAGE_TYPES = ["pdf"]
ALLOWED_DOC_TYPES = ["docx"]
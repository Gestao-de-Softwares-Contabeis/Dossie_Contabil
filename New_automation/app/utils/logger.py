"""
Configuração centralizada de logging usando loguru.
"""
import sys
from loguru import logger

# Remove o handler padrão
logger.remove()

# Console — nível INFO em produção
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> — <level>{message}</level>",
    colorize=True,
)

# Arquivo rotativo — mantém 7 dias
logger.add(
    "logs/app.log",
    rotation="00:00",
    retention="7 days",
    level="DEBUG",
    encoding="utf-8",
)

__all__ = ["logger"]
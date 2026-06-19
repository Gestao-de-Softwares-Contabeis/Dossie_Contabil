"""
Constantes estáticas da aplicação.
"""

MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
}

# Placeholders no template DOCX
PLACEHOLDER_DRE = "[[DEMONSTR_RESULTADO]]"
PLACEHOLDER_NOTAS = "[[EXP_DEMONSTR]]"
PLACEHOLDER_CARTA = "[[CARTA_RESP]]"

# Chaves dos uploads esperados pela UI
UPLOAD_KEYS = {
    "balanco": "balanco_file",
    "dre": "demstr_result_file",
    "notas": "explic_demonstr_file",
    "carta": "carta_responsb_file",
}

# Nome do arquivo de saída
OUTPUT_FILENAME_TEMPLATE = "Dossie_Contabil_{nome_empresa}.docx"
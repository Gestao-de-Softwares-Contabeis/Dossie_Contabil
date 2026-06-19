"""
Orquestração da geração do dossiê contábil.
"""
import datetime
import json
import tempfile
from io import BytesIO
from pathlib import Path
from typing import Optional

import requests
from docx import Document
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches

from app.core.file_processor import FileProcessor
from app.utils.logger import logger
from config.constants import (
    MESES_PT,
    PLACEHOLDER_DRE,
    PLACEHOLDER_NOTAS,
    PLACEHOLDER_CARTA,
    OUTPUT_FILENAME_TEMPLATE,
)
from config.settings import (
    TEMPLATE_PATH,
    N8N_WEBHOOK_URL,
    N8N_ENABLED,
    IMAGE_WIDTH_INCHES,
)


class DossieAutomation:
    """
    Gera o dossiê contábil completo a partir dos dados e uploads fornecidos.
    """

    def __init__(self):
        self._processor = FileProcessor()

    # ------------------------------------------------------------------ #
    # Geração do documento                                                  #
    # ------------------------------------------------------------------ #

    def generate(self, input_data: dict) -> tuple[Optional[bytes], Optional[str]]:
        """
        Orquestra a geração do dossiê.

        Args:
            input_data: Dicionário com chaves de metadados e 'uploads' (dict de UploadedFiles).

        Returns:
            (bytes_do_docx, None) em caso de sucesso, ou (None, mensagem_de_erro).
        """
        temp_paths: dict[str, str] = {}

        try:
            # 1. Salvar uploads em disco temporário
            for key, uploaded_file in input_data["uploads"].items():
                if uploaded_file is None:
                    return None, f"O arquivo '{key}' é obrigatório."
                temp_paths[key] = self._processor.save_upload_to_temp(uploaded_file)

            # 2. Renderizar template via docxtpl
            rendered_path = self._render_template(input_data, temp_paths)

            # 3. Inserir conteúdo dinâmico (PDF + DOCX) nos placeholders
            final_doc = Document(rendered_path)
            self._processor.insert_pdf_at_placeholder(
                final_doc, PLACEHOLDER_DRE, temp_paths["demstr_result_file"]
            )
            self._processor.insert_docx_at_placeholder(
                final_doc, PLACEHOLDER_NOTAS, temp_paths["explic_demonstr_file"]
            )
            self._processor.insert_docx_at_placeholder(
                final_doc, PLACEHOLDER_CARTA, temp_paths["carta_responsb_file"]
            )

            # 4. Serializar para bytes
            buffer = BytesIO()
            final_doc.save(buffer)
            buffer.seek(0)
            logger.info(f"Dossiê gerado com sucesso para '{input_data['nome_empresa']}'.")
            return buffer.getvalue(), None

        except ValueError as exc:
            logger.warning(str(exc))
            return None, str(exc)
        except FileNotFoundError as exc:
            msg = f"Template não encontrado em '{TEMPLATE_PATH}'. Verifique se o arquivo existe no repositório."
            logger.error(msg)
            return None, msg
        except Exception as exc:
            logger.exception("Erro inesperado durante geração do dossiê.")
            return None, f"Erro durante a geração: {exc}"
        finally:
            self._processor.cleanup_temp_files(*temp_paths.values())

    # ------------------------------------------------------------------ #
    # Internos                                                              #
    # ------------------------------------------------------------------ #

    def _render_template(self, input_data: dict, temp_paths: dict) -> str:
        """Renderiza o template DOCX com os dados e retorna o caminho do arquivo renderizado."""
        doc = DocxTemplate(str(TEMPLATE_PATH))

        pt1_bytes, pt2_bytes = self._processor.pdf_balanco_duas_paginas(
            temp_paths["balanco_file"]
        )

        context = {
            "nome_empresa": input_data["nome_empresa"],
            "data_atual": self._data_atual_formatada(),
            "periodo_anual": input_data["periodo_anual"],
            "cnpj_empresa": input_data["cnpj_empresa"],
            "data_dem_encerradas": input_data["data_dem_encerradas"],
            "razao_social_empresa": input_data["razao_social_empresa"],
            "periodo_em_data": input_data["periodo_em_data"],
            "balanco_patrimonial_pt1": InlineImage(doc, BytesIO(pt1_bytes), width=Inches(IMAGE_WIDTH_INCHES)),
            "balanco_patrimonial_pt2": InlineImage(doc, BytesIO(pt2_bytes), width=Inches(IMAGE_WIDTH_INCHES)),
            "demontr_resultado": PLACEHOLDER_DRE,
            "socios": input_data["socios"],
            "explic_demonstr": PLACEHOLDER_NOTAS,
            "carta_responsb": PLACEHOLDER_CARTA,
        }

        doc.render(context)

        rendered_path = str(Path(tempfile.gettempdir()) / "temp_rendered.docx")
        doc.save(rendered_path)
        return rendered_path

    @staticmethod
    def _data_atual_formatada() -> str:
        now = datetime.datetime.now()
        return f"{now.day} de {MESES_PT[now.month]} de {now.year}"

    # ------------------------------------------------------------------ #
    # Integração n8n                                                        #
    # ------------------------------------------------------------------ #

    def send_to_n8n(self, input_data: dict, file_bytes: bytes) -> tuple[bool, str]:
        """
        Envia metadados e o arquivo gerado para o webhook n8n.

        Returns:
            (True, mensagem_de_sucesso) ou (False, mensagem_de_erro).
        """
        if not N8N_ENABLED:
            return True, "Integração n8n desabilitada (N8N_ENABLED=false)."

        nome_arquivo = OUTPUT_FILENAME_TEMPLATE.format(nome_empresa=input_data["nome_empresa"])
        payload = {
            "nome_empresa": input_data["nome_empresa"],
            "razao_social_empresa": input_data["razao_social_empresa"],
            "cnpj_empresa": input_data["cnpj_empresa"],
            "periodo_anual": input_data["periodo_anual"],
            "periodo_em_data": input_data["periodo_em_data"],
            "data_dem_encerradas": input_data["data_dem_encerradas"],
            "socios": json.dumps(input_data["socios"]),
        }
        files = {
            "arquivo_dossie": (
                nome_arquivo,
                file_bytes,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        }

        try:
            response = requests.post(N8N_WEBHOOK_URL, data=payload, files=files, timeout=30)
            if response.ok:
                logger.info("Dossiê enviado ao n8n com sucesso.")
                return True, "Automação disparada no n8n com sucesso!"
            else:
                msg = f"n8n retornou status {response.status_code}."
                logger.warning(msg)
                return False, msg
        except requests.exceptions.RequestException as exc:
            msg = f"Falha ao conectar com n8n: {exc}"
            logger.error(msg)
            return False, msg
"""
Orquestração da geração do dossiê contábil.
"""
import datetime
import json
import tempfile
from io import BytesIO
from pathlib import Path
from typing import Optional

import jinja2
import requests
from docx import Document
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches

from core.file_processor import FileProcessor
from utils.helpers import format_cnpj
from utils.logger import logger
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
    # Geração do documento                                               #
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
                # O n8n retorna caminhos de arquivo (str) para notas/carta; uploads reais do
                # Streamlit chegam como UploadedFile e precisam ser salvos em disco.
                if isinstance(uploaded_file, str):
                    temp_paths[key] = uploaded_file
                else:
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

    # O template .docx foi criado para docxtemplater (JS) e usa tags de chave simples
    # ("{nome_empresa}"), não a sintaxe Jinja2 padrão do docxtpl ("{{ nome_empresa }}").
    # Configuramos o próprio Jinja2 para reconhecer chave simples em vez de editar o .docx.
    _JINJA_ENV = jinja2.Environment(variable_start_string="{", variable_end_string="}")

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
            # Aceita o CNPJ tanto já formatado quanto apenas com dígitos: format_cnpj
            # limpa e reaplica a máscara XX.XXX.XXX/XXXX-XX antes da substituição no
            # documento, independente de quem chamou generate() (UI ou n8n).
            "cnpj_empresa": format_cnpj(input_data["cnpj_empresa"]),
            "data_dem_encerradas": input_data["data_dem_encerradas"],
            "razao_social_empresa": input_data["razao_social_empresa"],
            "periodo_em_data": input_data["periodo_em_data"],
            "balanco_patrimonial_pt1": InlineImage(doc, BytesIO(pt1_bytes), width=Inches(IMAGE_WIDTH_INCHES)),
            "balanco_patrimonial_pt2": InlineImage(doc, BytesIO(pt2_bytes), width=Inches(IMAGE_WIDTH_INCHES)),
            "dre_img": PLACEHOLDER_DRE,
            "socios_assinaturas": self._formatar_socios_assinaturas(input_data["socios"]),
            "explic_demonstr": PLACEHOLDER_NOTAS,
            "carta_responsb": PLACEHOLDER_CARTA,
            # Resquício do template original em docxtemplater: uma tag ficou como
            # "{d.periodo_anual}" em vez de "{periodo_anual}". Em vez de editar o .docx
            # (risco de quebrar runs/formatação no Word), expomos o mesmo valor sob "d".
            "d": {"periodo_anual": input_data["periodo_anual"]},
        }

        # autoescape=True é obrigatório aqui: é o que faz o docxtpl reconhecer
        # RichText/RichTextParagraph/InlineImage e injetar o XML deles corretamente
        # (sem isso, esses objetos viram texto puro via str() e corrompem o XML do docx).
        # Também escapa caracteres especiais de XML (&, <, >) em textos livres, o que é
        # necessário de qualquer forma para o documento final ser um XML válido.
        doc.render(context, self._JINJA_ENV, autoescape=True)

        rendered_path = str(Path(tempfile.gettempdir()) / "temp_rendered.docx")
        doc.save(rendered_path)
        return rendered_path

    @staticmethod
    def _data_atual_formatada() -> str:
        now = datetime.datetime.now()
        return f"{now.day} de {MESES_PT[now.month]} de {now.year}"

    @staticmethod
    def _formatar_socios_assinaturas(socios: list[dict]) -> str:
        """
        Monta o bloco de assinatura de cada sócio no padrão:
            _______________________________
            NOME EM MAIÚSCULO
            Cargo
            CPF: xxx.xxx.xxx-xx
        Retorna uma string simples com quebras de linha reais ("\\n"): o placeholder no
        template fica sozinho dentro de um único "<w:t>", então qualquer XML de run
        (como um RichText customizado com "<w:r>"/"<w:br/>") acaba sendo inserido
        ANINHADO dentro desse "<w:t>" — o que não é um XML válido ("<w:t>" só aceita
        texto). Isso corrompe o documento e, com mais de um sócio, o LibreOffice/Word
        chega a descartar os blocos seguintes silenciosamente. Usando "\\n" comum, o
        próprio docxtpl converte cada um em "</w:t><w:br/><w:t>" no pós-processamento
        (ver resolve_listing em docxtpl/template.py), que é estruturalmente válido.
        """
        socios_validos = [s for s in socios if s.get("nome")]
        blocos = []

        for socio in socios_validos:
            linhas = [
                "_" * 35,
                socio.get("nome", "").upper(),
                socio.get("cargo", ""),
                f"CPF: {socio.get('cpf', '')}",
            ]
            blocos.append("\n".join(linhas))

        return "\n\n".join(blocos)

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
"""
Testes unitários para FileProcessor.
"""
import io
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open

import pytest

from app.core.file_processor import FileProcessor


class TestFileProcessor:
    """Suite de testes para FileProcessor."""

    @pytest.fixture
    def processor(self) -> FileProcessor:
        return FileProcessor()

    # ------------------------------------------------------------------ #
    # validate_file                                                          #
    # ------------------------------------------------------------------ #

    def test_validate_file_docx(self, processor):
        assert processor.validate_file("relatorio.docx") is True

    def test_validate_file_pdf(self, processor):
        assert processor.validate_file("balanco.pdf") is True

    def test_validate_file_png(self, processor):
        assert processor.validate_file("imagem.png") is True

    def test_validate_file_invalid_extension(self, processor):
        assert processor.validate_file("arquivo.xls") is False

    def test_validate_file_no_extension(self, processor):
        assert processor.validate_file("sem_extensao") is False

    def test_validate_file_case_insensitive(self, processor):
        assert processor.validate_file("BALANCO.PDF") is True

    # ------------------------------------------------------------------ #
    # save_upload_to_temp                                                    #
    # ------------------------------------------------------------------ #

    def test_save_upload_to_temp_creates_file(self, processor):
        mock_upload = MagicMock()
        mock_upload.name = "teste.pdf"
        mock_upload.getvalue.return_value = b"conteudo fake"

        path = FileProcessor.save_upload_to_temp(mock_upload)

        try:
            assert os.path.exists(path)
            assert Path(path).suffix == ".pdf"
            assert Path(path).read_bytes() == b"conteudo fake"
        finally:
            os.remove(path)

    # ------------------------------------------------------------------ #
    # cleanup_temp_files                                                     #
    # ------------------------------------------------------------------ #

    def test_cleanup_removes_files(self, processor):
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp.close()
        assert os.path.exists(tmp.name)

        FileProcessor.cleanup_temp_files(tmp.name)

        assert not os.path.exists(tmp.name)

    def test_cleanup_ignores_none(self, processor):
        """Não deve lançar exceção ao receber None."""
        FileProcessor.cleanup_temp_files(None, None)

    def test_cleanup_ignores_missing_file(self, processor):
        """Não deve lançar exceção para caminhos inexistentes."""
        FileProcessor.cleanup_temp_files("/caminho/inexistente.docx")

    # ------------------------------------------------------------------ #
    # pdf_balanco_duas_paginas                                               #
    # ------------------------------------------------------------------ #

    def test_pdf_balanco_raises_if_less_than_2_pages(self, processor):
        """Deve lançar ValueError se o PDF tiver menos de 2 páginas."""
        with patch.object(processor, "pdf_to_images", return_value=[b"pagina1"]):
            with pytest.raises(ValueError, match="pelo menos 2 páginas"):
                processor.pdf_balanco_duas_paginas("qualquer.pdf")

    def test_pdf_balanco_returns_two_pages(self, processor):
        fake_images = [b"pg1", b"pg2", b"pg3"]
        with patch.object(processor, "pdf_to_images", return_value=fake_images):
            pt1, pt2 = processor.pdf_balanco_duas_paginas("qualquer.pdf")
        assert pt1 == b"pg1"
        assert pt2 == b"pg2"
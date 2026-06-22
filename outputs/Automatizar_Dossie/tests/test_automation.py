"""
Testes unitários para DossieAutomation.
"""
from unittest.mock import MagicMock, patch

import pytest

from app.core.automation import DossieAutomation


@pytest.fixture
def automation() -> DossieAutomation:
    return DossieAutomation()


@pytest.fixture
def base_input() -> dict:
    """Payload mínimo válido para geração."""
    mock_file = MagicMock()
    mock_file.name = "arquivo.pdf"
    mock_file.getvalue.return_value = b"fake"

    mock_docx = MagicMock()
    mock_docx.name = "arquivo.docx"
    mock_docx.getvalue.return_value = b"fake"

    return {
        "nome_empresa": "Empresa Teste",
        "razao_social_empresa": "Empresa Teste Ltda",
        "cnpj_empresa": "00.000.000/0001-00",
        "periodo_anual": "Janeiro a Dezembro de 2024",
        "periodo_em_data": "01 a 12/24",
        "data_dem_encerradas": "31/12/2024",
        "socios": [{"nome": "Sócio 1", "cpf": "000.000.000-00", "cargo": "Diretor"}],
        "uploads": {
            "balanco_file": mock_file,
            "demstr_result_file": mock_file,
            "explic_demonstr_file": mock_docx,
            "carta_responsb_file": mock_docx,
        },
    }


class TestDossieAutomation:
    def test_generate_returns_error_if_upload_missing(self, automation, base_input):
        base_input["uploads"]["balanco_file"] = None
        file_bytes, error = automation.generate(base_input)
        assert file_bytes is None
        assert error is not None
        assert "obrigatório" in error.lower()

    def test_send_to_n8n_disabled(self, automation, base_input):
        with patch("app.core.automation.N8N_ENABLED", False):
            ok, msg = automation.send_to_n8n(base_input, b"bytes")
        assert ok is True
        assert "desabilitada" in msg.lower()

    def test_send_to_n8n_success(self, automation, base_input):
        mock_response = MagicMock()
        mock_response.ok = True

        with patch("app.core.automation.N8N_ENABLED", True), \
             patch("requests.post", return_value=mock_response):
            ok, msg = automation.send_to_n8n(base_input, b"bytes")

        assert ok is True

    def test_send_to_n8n_failure(self, automation, base_input):
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 500

        with patch("app.core.automation.N8N_ENABLED", True), \
             patch("requests.post", return_value=mock_response):
            ok, msg = automation.send_to_n8n(base_input, b"bytes")

        assert ok is False
        assert "500" in msg
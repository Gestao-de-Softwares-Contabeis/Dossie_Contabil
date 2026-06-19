"""
Interface Streamlit do Gerador de Dossiês Contábeis.
Ponto de entrada para `streamlit run app/main.py`.
"""
import datetime

import streamlit as st

from app.core.automation import DossieAutomation
from app.utils.helpers import (
    format_cnpj,
    format_cpf,
    clean_numbers,
    build_periodo_em_data,
    build_periodo_anual,
)
from config.constants import OUTPUT_FILENAME_TEMPLATE

# ------------------------------------------------------------------ #
# Configuração da página                                                #
# ------------------------------------------------------------------ #
st.set_page_config(
    page_title="Gerador de Dossiês Contábeis",
    page_icon="📄",
    layout="wide",
)

st.title("📄 Gerador Automático de Dossiês Contábeis")
st.markdown("Preencha os campos e faça o upload dos arquivos para gerar o documento final.")

# ------------------------------------------------------------------ #
# Inicialização de estado                                               #
# ------------------------------------------------------------------ #
if "socios" not in st.session_state:
    st.session_state.socios = [{"nome": "", "cpf": "", "cargo": ""}]

# ------------------------------------------------------------------ #
# Abas                                                                  #
# ------------------------------------------------------------------ #
tab1, tab2, tab3 = st.tabs(
    ["🏢 Dados da Empresa / Períodos", "👥 Dados dos Sócios", "📎 Upload de Arquivos"]
)

input_data: dict = {"uploads": {}}

# ── Aba 1 ─────────────────────────────────────────────────────────── #
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        input_data["nome_empresa"] = st.text_input("Nome Fantasia da Empresa")
        input_data["razao_social_empresa"] = st.text_input("Razão Social")
        cnpj_raw = st.text_input("CNPJ (somente números)")
        input_data["cnpj_empresa"] = format_cnpj(cnpj_raw)
        if cnpj_raw:
            st.caption(f"Formatado: `{input_data['cnpj_empresa']}`")

    with col2:
        st.markdown("##### Período de Referência Contábil")
        today = datetime.date.today()
        data_inicio = st.date_input(
            "Data de Início",
            value=datetime.date(today.year, 1, 1),
            min_value=datetime.date(1980, 1, 1),
            max_value=today,
            key="data_inicio",
        )
        data_fim = st.date_input(
            "Data de Fim",
            value=today,
            min_value=datetime.date(1980, 1, 1),
            max_value=today,
            key="data_fim",
        )

        input_data["periodo_em_data"] = build_periodo_em_data(data_inicio, data_fim)
        input_data["periodo_anual"] = build_periodo_anual(data_inicio, data_fim)
        input_data["data_dem_encerradas"] = data_fim.strftime("%d/%m/%Y")

        st.markdown("---")
        st.caption(f"Período curto: `{input_data['periodo_em_data']}`")
        st.caption(f"Período longo: `{input_data['periodo_anual']}`")

# ── Aba 2 ─────────────────────────────────────────────────────────── #
with tab2:
    st.subheader("Dados dos Sócios / Administradores")

    for i, socio in enumerate(st.session_state.socios):
        with st.expander(f"Sócio {i + 1}", expanded=True):
            socio["nome"] = st.text_input(f"Nome completo", value=socio["nome"], key=f"nome_{i}")
            cpf_raw = st.text_input(f"CPF (somente números)", value=clean_numbers(socio["cpf"]), key=f"cpf_{i}")
            st.session_state.socios[i]["cpf"] = format_cpf(cpf_raw)
            if cpf_raw:
                st.caption(f"Formatado: `{st.session_state.socios[i]['cpf']}`")
            socio["cargo"] = st.text_input(f"Cargo", value=socio["cargo"], key=f"cargo_{i}")

            if st.button(f"🗑️ Remover Sócio {i + 1}", key=f"remove_{i}"):
                st.session_state.socios.pop(i)
                st.rerun()

    if st.button("➕ Adicionar Sócio"):
        st.session_state.socios.append({"nome": "", "cpf": "", "cargo": ""})
        st.rerun()

    input_data["socios"] = st.session_state.socios

# ── Aba 3 ─────────────────────────────────────────────────────────── #
with tab3:
    st.subheader("Balanço e DRE (PDF)")
    col5, col6 = st.columns(2)
    with col5:
        input_data["uploads"]["balanco_file"] = st.file_uploader(
            "Balanço Patrimonial (PDF — mínimo 2 páginas)", type=["pdf"]
        )
    with col6:
        input_data["uploads"]["demstr_result_file"] = st.file_uploader(
            "Demonstração do Resultado — DRE (PDF)", type=["pdf"]
        )

    st.subheader("Notas e Carta (DOCX)")
    col7, col8 = st.columns(2)
    with col7:
        input_data["uploads"]["explic_demonstr_file"] = st.file_uploader(
            "Notas Explicativas (DOCX — sem título interno)", type=["docx"], key="notas"
        )
    with col8:
        input_data["uploads"]["carta_responsb_file"] = st.file_uploader(
            "Carta de Responsabilidade (DOCX — sem título interno)", type=["docx"], key="carta"
        )

# ------------------------------------------------------------------ #
# Botão de geração                                                      #
# ------------------------------------------------------------------ #
st.divider()
if st.button("✅ GERAR DOSSIÊ CONTÁBIL", type="primary", use_container_width=True):
    required = ["balanco_file", "demstr_result_file", "explic_demonstr_file", "carta_responsb_file"]
    missing = [k for k in required if not input_data["uploads"].get(k)]

    if missing:
        st.warning(f"Arquivo(s) obrigatório(s) pendente(s): {', '.join(missing)}")
    elif not input_data.get("nome_empresa"):
        st.warning("Informe o Nome Fantasia da empresa antes de gerar.")
    else:
        automation = DossieAutomation()

        with st.spinner("Gerando dossiê… aguarde."):
            file_bytes, error = automation.generate(input_data)

        if error:
            st.error(f"❌ Falha: {error}")
        else:
            st.success("✅ Dossiê gerado com sucesso!")
            filename = OUTPUT_FILENAME_TEMPLATE.format(nome_empresa=input_data["nome_empresa"])
            st.download_button(
                label="⬇️ Baixar Dossiê (.docx)",
                data=file_bytes,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

            with st.spinner("Enviando para o n8n…"):
                ok, msg = automation.send_to_n8n(input_data, file_bytes)
            if ok:
                st.info(f"➡️ {msg}")
            else:
                st.warning(f"⚠️ n8n: {msg}")
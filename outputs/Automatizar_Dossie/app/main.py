"""
Interface Streamlit do Gerador de Dossiês Contábeis.
Ponto de entrada para `streamlit run app/main.py`.
"""
import datetime
import requests
import tempfile
from pathlib import Path
from docx import Document

import sys
from pathlib import Path

raiz_projeto = Path(__file__).resolve().parent.parent
if str(raiz_projeto) not in sys.path:
    sys.path.append(str(raiz_projeto))

import streamlit as st

from core.automation import DossieAutomation
from utils.helpers import (
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
tab1, tab2, tab3, tab4 = st.tabs(
    ["🏢 Empresa / Períodos", "👥 Sócios", "📎 Uploads", "⚠️ Pendências e Ressalvas"]
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

# ── Aba 4: Pendências (Substituindo o Telegram) ───────────────────── #
with tab4:
    st.subheader("Análise de Ressalvas e Pendências")
    st.markdown("Selecione se alguma pendência ou situação específica se aplica ao cenário atual da empresa.")
    
    OPCOES_PENDENCIAS = [
        "1. DISPONIBILIDADES – CAIXA", "2. DISPONIBILIDADES – CONTAS BANCÁRIAS", 
        "3. APLICAÇÕES FINANCEIRAS", "4. CONTAS A RECEBER (CLIENTES)", 
        "5. TRANSAÇÕES COM PARTES RELACIONADAS (SÓCIOS)", "6. ADIANTAMENTO A FORNECEDORES", 
        "7. ADIANTAMENTOS A EMPREGADOS", "8. RECUPERAÇÃO DE TRIBUTOS", 
        "9. SALDOS INICIAIS (BALANÇO DE ABERTURA)", "10. ESTOQUES", 
        "11. CONTROLE DE ESTOQUES EM PODER DE TERCEIROS", "12. ATIVO IMOBILIZADO", 
        "13. DEPRECIAÇÃO E VIDA ÚTIL (CPC 27)", "14. FORNECEDORES (PASSIVO CIRCULANTE)", 
        "15. OBRIGAÇÕES TRIBUTÁRIAS", "16. CONCILIAÇÃO DE FOLHA DE PAGAMENTO", 
        "17. CONFUSÃO PATRIMONIAL (PRINCÍPIO DA ENTIDADE)", "18. PASSIVO A DESCOBERTO / OMISSÃO DE RECEITA", 
        "19. DISPÊNDIOS SEM COMPROVAÇÃO FISCAL", "20. PASSIVOS ONEROSOS (EMPRÉSTIMOS)", 
        "21. CONSÓRCIOS", "22. DESPESAS ANTECIPADAS (SEGUROS)", 
        "23. PARCELAMENTOS TRIBUTÁRIOS", "24. ARRENDAMENTO MERCANTIL E ALUGUÉIS (CPC 06)", 
        "25. OBRIGAÇÕES COM CARTÕES DE CRÉDITO", "Nenhuma das Opções"
    ]
    
    input_data["pendencias"] = st.multiselect(
        "Selecione as pendências ou ressalvas aplicáveis:", 
        options=OPCOES_PENDENCIAS,
        default=["Nenhuma das Opções"]
    )

# ------------------------------------------------------------------ #
# Botão de geração                                                      #
# ------------------------------------------------------------------ #
st.divider()
if st.button("✅ GERAR DOSSIÊ CONTÁBIL", type="primary", use_container_width=True):
    # Exigimos apenas os PDFs de Balanço e DRE agora
    required = ["balanco_file", "demstr_result_file"]
    missing = [k for k in required if not input_data["uploads"].get(k)]

    if missing:
        st.warning(f"Arquivo(s) obrigatório(s) pendente(s): {', '.join(missing)}")
    elif not input_data.get("nome_empresa"):
        st.warning("Informe o Nome Fantasia da empresa antes de gerar.")
    else:
        automation = DossieAutomation()

        with st.spinner("Conectando ao n8n para gerar Notas e Carta (isso pode levar 1-2 minutos)…"):
            # 1. Prepara a chamada para o n8n
            N8N_WEBHOOK_URL = "https://genai.up4me.io/webhook/receber-dados" 
            
            # ATUALIZAÇÃO: Enviando todos os dados que o n8n espera ler no JSON do body
            payload = {
                "nome_empresa": input_data.get("nome_empresa", ""),
                "razao_social_empresa": input_data.get("razao_social_empresa", ""),
                "cnpj_empresa": input_data.get("cnpj_empresa", ""),
                "periodo_em_data": input_data.get("periodo_em_data", ""),
                "periodo_anual": input_data.get("periodo_anual", ""),
                "data_dem_encerradas": input_data.get("data_dem_encerradas", ""),
                "pendencias": input_data.get("pendencias", []),
                "socios": input_data.get("socios", [])
            }
            
            # Extraímos os objetos de arquivo do Streamlit
            balanco_file = input_data["uploads"]["balanco_file"]
            dre_file = input_data["uploads"]["demstr_result_file"]

            # Montamos o dicionário usando a estrutura de tupla exigida pelo requests:
            # (nome_do_arquivo, conteudo_em_bytes, tipo_mime)
            files = {
                "balanco": (balanco_file.name, balanco_file.getvalue(), balanco_file.type),
                "dre": (dre_file.name, dre_file.getvalue(), dre_file.type)
            }
            
            try:
                # Faz o POST e ESPERA a resposta do n8n
                response = requests.post(N8N_WEBHOOK_URL, data=payload, files=files, timeout=180)
                
                if response.ok:
                    dados_gerados = response.json()
                    notas_texto = dados_gerados.get("notas", "Erro ao gerar notas")
                    carta_texto = dados_gerados.get("carta", "Erro ao gerar carta")
                    
                    st.success("✨ Textos gerados pelo n8n com sucesso! Montando dossiê...")
                    
                    # 2. Converte os textos retornados em arquivos DOCX temporários para o Automation
                    doc_notas = Document()
                    doc_notas.add_paragraph(notas_texto)
                    path_notas = Path(tempfile.gettempdir()) / "temp_notas.docx"
                    doc_notas.save(path_notas)
                    
                    doc_carta = Document()
                    doc_carta.add_paragraph(carta_texto)
                    path_carta = Path(tempfile.gettempdir()) / "temp_carta.docx"
                    doc_carta.save(path_carta)
                    
                    # Injeta os caminhos no input_data para simular o upload que foi comentado
                    # Você precisará ajustar o `automation.generate` para aceitar caminhos caso ele espere "UploadedFiles"
                    input_data["uploads"]["explic_demonstr_file_path"] = str(path_notas)
                    input_data["uploads"]["carta_responsb_file_path"] = str(path_carta)
                    
                    # 3. Gera o arquivo final
                    file_bytes, error = automation.generate(input_data)
                    
                    if error:
                        st.error(f"❌ Falha na montagem final: {error}")
                    else:
                        st.success("✅ Dossiê completo montado!")
                        filename = OUTPUT_FILENAME_TEMPLATE.format(nome_empresa=input_data["nome_empresa"])
                        st.download_button(
                            label="⬇️ Baixar Dossiê Completo (.docx)",
                            data=file_bytes,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        )
                else:
                    st.error(f"❌ Erro do n8n: {response.status_code} - {response.text}")
                    
            except requests.exceptions.Timeout:
                st.error("O n8n demorou muito para responder (Timeout).")
            except Exception as e:
                st.error(f"Erro na comunicação com n8n: {e}")
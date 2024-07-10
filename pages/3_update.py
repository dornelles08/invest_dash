import streamlit as st

from functions.get_fii_details import get_fii
from functions.load_data import get_fiis_infos, load_fiis
from services.dados import DadosService
from services.fiis import FiisService

if "token" not in st.session_state or st.session_state.token is None or \
        "user" not in st.session_state or st.session_state.user is None:
    st.session_state["token"] = None
    st.session_state["user"] = None
    st.switch_page("1_home.py")

fiis_service = FiisService()
dados_service = DadosService()

st.header("Atualizar informações sobre oa Ativos", divider=True)

if st.button("Atualizar Base"):
    fiis_infos = get_fiis_infos(st, st.session_state["user"]["_id"])
    dados_service.upsert_dados(fiis_infos)
    st.write("Informações atualizadas")


st.header("Adicionar Novo Ativo", divider=True)
col1, col2, col3 = st.columns([1, 1, 1])
new_ativo = col1.text_input("Nome do Novo Ativo")
new_qtd_ativo = col2.number_input(
    "Quantidade do Novo Ativo",  value=None, min_value=0)
new_category_ativo = col3.text_input("Categoria do Novo Ativo")

if st.button("Adicionar Ativo"):
    fii_infos = get_fii(new_ativo)
    dados_service.upsert_dado(fii_infos)
    fiis_service.upsert_fii({
        "ativo": new_ativo,
        "qtd": new_qtd_ativo,
        "category": new_category_ativo,
        "user_id": st.session_state["user"]["_id"]
    })
    st.write("Ativo adicionado")
    st.session_state["dados"] = None


st.header("Atualizar Quantidade de um Ativo", divider=True)
_, fiis_category, fiis_names, fiis_qtd = load_fiis(
    st.session_state["user"]["_id"])
col1, col2, col3 = st.columns([1, 1, 1])
ativo = col1.selectbox("Fii", fiis_names)
if ativo:
    qtd_ativo = col2.number_input(
        "Quantidade do Ativo",  value=fiis_qtd[ativo], min_value=0)
    category_ativo = col3.text_input(
        "Categoria do Ativo", fiis_category[ativo])

    if st.button("Atualizar Ativo"):
        fiis, _, _, _ = load_fiis(st.session_state["user"]["_id"])
        fiis_service.update_fii({
            "ativo": ativo,
            "qtd": qtd_ativo,
            "category": category_ativo
        })

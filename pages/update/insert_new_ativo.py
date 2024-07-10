import streamlit as st

from functions.configs import valid_user_logged
from functions.get_fii_details import get_fii
from services.dados import DadosService
from services.fiis import FiisService

valid_user_logged()


fiis_service = FiisService()
dados_service = DadosService()

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

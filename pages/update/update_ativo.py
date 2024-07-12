import streamlit as st

from functions.configs import valid_user_logged
from functions.load_data import load_fiis
from services.fiis import FiisService

valid_user_logged()

fiis_service = FiisService()

st.header("Atualizar Ativo", divider=True)
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
        st.success('Ativo atualizado com sucesso', icon="✅")

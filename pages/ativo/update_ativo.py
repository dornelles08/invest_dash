import streamlit as st

from functions.configs import valid_user_logged
from functions.load_data import load_fiis
from services.fiis import FiisService

valid_user_logged()

fiis_service = FiisService()

st.header("Atualizar Ativo", divider=True)
_, fiis_category, fiis_names = load_fiis(
    st.session_state["user"]["_id"])

col1, col2, _ = st.columns([1, 1, 1])
ativo = col1.selectbox("Fii", fiis_names)
if ativo:
    category_ativo = col2.text_input(
        "Categoria do Ativo", fiis_category[ativo])

    if st.button("Atualizar Ativo"):
        fiis_service.update_fii({
            "ativo": ativo,
            "category": category_ativo,
            "user_id": st.session_state["user"]["_id"]
        })
        st.success('Ativo atualizado com sucesso', icon="✅")
        st.session_state["dados"] = None

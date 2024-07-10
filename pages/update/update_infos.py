import streamlit as st

from functions.load_data import get_fiis_infos
from services.dados import DadosService

if "token" not in st.session_state or st.session_state.token is None or \
        "user" not in st.session_state or st.session_state.user is None:
    st.session_state["token"] = None
    st.session_state["user"] = None
    st.switch_page("home.py")

dados_service = DadosService()

st.header("Atualizar informações dos Ativos", divider=True)

if st.button("Atualizar Base"):
    fiis_infos = get_fiis_infos(st, st.session_state["user"]["_id"])
    dados_service.upsert_dados(fiis_infos)
    st.write("Informações atualizadas")

from datetime import datetime

import streamlit as st

from functions.configs import valid_user_logged
from functions.load_data import get_fiis_infos
from services.dados import DadosService
from services.user import UserService

valid_user_logged()

dados_service = DadosService()
user_services = UserService()

st.header("Atualizar Base", divider=True)

if st.button("Atualizar Base"):
    if (datetime.strptime(st.session_state["user"]["sync"], "%x %X") - datetime.now()).seconds <= 900:
        fiis_infos = get_fiis_infos(st, st.session_state["user"]["_id"])
        dados_service.upsert_dados(fiis_infos)
        user_services.update_user({
            **st.session_state["user"],
            "sync": datetime.now().strftime("%x %X")
        })
    st.write("Informações atualizadas")

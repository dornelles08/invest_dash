"""
    Funções para configurações das paginas
"""
import streamlit as st

from functions.login import valid_token


def config_header(title, icon):
    """
        Função configurar o cabeçalho das paginas
    """
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout="wide",
    )


def valid_user_logged():
    if "token" not in st.session_state or st.session_state.token is None or \
            "user" not in st.session_state or st.session_state.user is None:
        st.session_state["token"] = None
        st.session_state["user"] = None
        st.switch_page("home.py")
    else:
        token_is_valid = valid_token(st.session_state["token"])
        if not token_is_valid:
            st.switch_page("home.py")

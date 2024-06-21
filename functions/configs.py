"""
    Funções para configurações das paginas
"""
import streamlit as st


def config_header(title, icon):
    """
        Função configurar o cabeçalho das paginas
    """
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout="wide",
    )

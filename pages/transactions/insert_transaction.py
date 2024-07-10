import streamlit as st

from functions.configs import valid_user_logged
from services.dados import DadosService
from services.transaction import TransactionsService

valid_user_logged()

transactions_service = TransactionsService()
dados_service = DadosService()

st.header("Adicionar Nova Transação", divider=True)

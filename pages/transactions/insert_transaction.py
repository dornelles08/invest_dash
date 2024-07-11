from datetime import datetime

import streamlit as st

from functions.configs import valid_user_logged
from services.dados import DadosService
from services.transaction import TransactionsService

valid_user_logged()

transactions_service = TransactionsService()
dados_service = DadosService()

st.header("Adicionar Nova Transação", divider=True)

form = st.form("new_transaction", clear_on_submit=True)

ativo = form.text_input("Ativo")
qtd = form.number_input(
    "Quantidade",  value=None, min_value=0)
price = form.number_input("Preço em R$", value=None, min_value=0)
date = form.date_input(
    "Data da Compra", datetime.now().date(), format="DD/MM/YYYY")

submmited = form.form_submit_button("Adicionar Transação")
if submmited:
    transaction = {
        "ativo": ativo,
        "qtd": qtd,
        "price": price,
        "date": date.strftime("%x"),
        "user_id": st.session_state["user"]["_id"]
    }
    transactions_service.insert_transaction(transaction)

    st.write("Transação adicionada")
    # st.session_state["dados"] = None
from datetime import datetime

import streamlit as st

from functions.configs import valid_user_logged
from services.transaction import TransactionsService

valid_user_logged()


@st.experimental_dialog("Adicionar Nova Transação")
def insert_transaction():
    transactions_service = TransactionsService()

    form = st.form("new_transaction", clear_on_submit=True)

    ativo = form.text_input("Ativo")
    qtd = form.number_input(
        "Quantidade",  value=None, min_value=0.00)
    price = form.number_input("Preço em R$", value=None, min_value=0.00)
    date = form.date_input(
        "Data da Compra", datetime.now().date(), format="DD/MM/YYYY")

    submmited = form.form_submit_button("Adicionar Transação")
    if submmited:
        transaction = {
            "ativo": ativo,
            "qtd": qtd,
            "price": price,
            "date": datetime.combine(date, datetime.min.time()),
            "total": qtd*price,
            "user_id": st.session_state["user"]["_id"]
        }
        transactions_service.insert_transaction(transaction)

        st.success("Transação Adicionada com Sucesso", icon="✅")
        st.session_state["dados"] = None
        st.rerun()

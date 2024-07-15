from datetime import datetime

import streamlit as st

from services.transaction import TransactionsService

st.header("Indicar Desdobramento", divider=True)

transactions_service = TransactionsService()

form = st.form("desdobramento", clear_on_submit=True)

fiis = transactions_service.get_fiis_from_transactions(
    st.session_state["user"]["_id"])

ativo = form.selectbox("Ativo", fiis)
date = form.date_input(
    "Data do Desdobramento", datetime.now().date(), format="DD/MM/YYYY")

submmited = form.form_submit_button("Desdobrar")
if submmited:
    transactions = transactions_service.get_transactions(
        st.session_state["user"]["_id"], {"ativo": ativo})

    for transaction in transactions:
        transaction_date = datetime.strptime(
            transaction["date"], "%d/%m/%y").date()
        if date > transaction_date:
            transactions_service.update_transaction({
                **transaction,
                "qtd": transaction["qtd"]*10,
                "price": transaction["price"]/10
            })

    st.success("Desdobramento Realizado com Sucesso", icon="✅")
    st.session_state["dados"] = None

import pandas as pd
import streamlit as st

from functions.configs import valid_user_logged
from pages.transactions.insert_transaction import insert_transaction
from services.transaction import TransactionsService

valid_user_logged()

transaction_service = TransactionsService()

st.header("Transações", divider=True)

if st.button("Adicionar nova transação"):
    insert_transaction()

transactions = transaction_service.get_transactions(
    st.session_state["user"]["_id"])

total_transactions = transaction_service.count_transactions(
    st.session_state["user"]["_id"])

transactions = pd.DataFrame(transactions, columns=[
                            '_id', 'ativo', 'qtd', 'price', 'date', 'total', 'user_id'])

transactions = transactions[["ativo", "qtd", "price", "date", "total"]]

transactions = transactions.rename(columns={
    "ativo": "Ativo",
    "qtd": "Quantidade",
    "price": "Preço",
    "total": "Total",
    "date": "Data da Compra",
})

transactions["Data da Compra"] = pd.to_datetime(
    transactions["Data da Compra"], format="%d/%m/%y")

transactions.sort_values(by="Data da Compra", ascending=False)

st.dataframe(transactions, hide_index=True, height=500, use_container_width=True,
             column_config={
                 "Preço": st.column_config.NumberColumn(format="R$ %.2f"),
                 "Total": st.column_config.NumberColumn(format="R$ %.2f"),
                 "Data da Compra": st.column_config.DateColumn(format="DD/MM/YYYY"),
             })

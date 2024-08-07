import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from functions.configs import valid_user_logged
from pages.transactions.edit_transaction import edit_transaction
from pages.transactions.insert_transaction import insert_transaction
from services.transaction import TransactionsService

valid_user_logged()


transaction_service = TransactionsService()

st.header("Transações", divider=True)

if st.button("Adicionar nova transação"):
    insert_transaction()

transactions = transaction_service.get_transactions(
    st.session_state["user"]["_id"], order_by="date")

total_transactions = transaction_service.count_transactions(
    st.session_state["user"]["_id"])

transactions = pd.DataFrame(transactions, columns=[
                            "_id", "ativo", "qtd", "price", "date", "total", "user_id"])

transactions = transactions[["ativo", "qtd", "price", "date", "total", "_id"]]

transactions = transactions.rename(columns={
    "ativo": "Ativo",
    "qtd": "Quantidade",
    "price": "Preço",
    "total": "Total",
    "date": "Data da Compra",
})

transactions["Data da Compra"] = pd.to_datetime(
    transactions["Data da Compra"], format="%d/%m/%y")

transactions["mesAno"] = transactions["Data da Compra"].dt.to_period("M")

transactions.sort_values(by="Data da Compra", ascending=True)

fiis_names = transaction_service.get_fiis_from_transactions(
    st.session_state["user"]["_id"])

col1, col2 = st.columns([1, 1])
ativo = col1.selectbox("Fii", fiis_names, index=None)

meses = list(transactions["mesAno"].unique())
ref = col2.selectbox("Mês Referência", meses, index=None)

if ativo:
    transactions = transactions[transactions["Ativo"] == ativo]
if ref:
    transactions = transactions[transactions["mesAno"] == ref]

event = st.dataframe(transactions, hide_index=True, height=500, use_container_width=True,
                     column_config={
                         "Preço": st.column_config.NumberColumn(format="R$ %.2f"),
                         "Total": st.column_config.NumberColumn(format="R$ %.2f"),
                         "Data da Compra": st.column_config.DateColumn(format="DD/MM/YYYY"),
                     },
                     on_select="rerun", selection_mode=["single-row"],
                     column_order=["Ativo",
                                   "Quantidade",
                                   "Preço",
                                   "Total",
                                   "Data da Compra",])

if len(event.selection.rows) > 0:
    row = event.selection.rows[0]
    edit_transaction(transactions.iloc[row].to_dict())
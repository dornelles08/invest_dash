import calendar
from datetime import datetime

import pandas as pd
import streamlit as st

from functions.load_data import load_fiis
from pages.dashboard.resume import resume
from pages.patrimonio.graphics import graphics
from services.dados import DadosService
from services.transaction import TransactionsService


def convert_date(data_str):
    return datetime.strptime(data_str, "%m/%Y")


def last_day_month(data_str):
    date = datetime.strptime(data_str, "%m/%Y")
    last_day = calendar.monthrange(date.year, date.month)[1]
    return datetime(date.year, date.month, last_day)


transaction_service = TransactionsService()
dados_service = DadosService()

transactions = transaction_service.get_transactions(
    st.session_state["user"]["_id"], order_by="date")

dates = [t["date"].strftime("%m/%Y") for t in transactions]
dates = list(set(dates))

dates.sort(key=convert_date, reverse=True)


col, _ = st.columns([1, 10])
ref = col.selectbox("Referência", dates)

st.header(f"Patrimônio em {ref}", divider=True)

ref_date = last_day_month(ref)

filtered_transactions = list(
    filter(lambda x: x["date"] < ref_date, transactions))


filtered_transactions = pd.DataFrame(filtered_transactions, columns=[
    '_id', 'ativo', 'qtd', 'price', 'date', 'total', 'user_id'])

filtered_transactions = filtered_transactions[[
    "ativo", "qtd", "price", "date", "total"]]

transactions_groups = filtered_transactions.groupby("ativo")
fiis = [ativo for ativo, _ in transactions_groups]

dados = dados_service.get_dados(fiis)

for ativo, df in transactions_groups:
    indice = next((index for (index, d) in enumerate(
        dados) if d["nome"] == ativo), None)

    if indice is not None:
        dados[indice] = {
            **dados[indice],
            "quantidade": df["qtd"].sum(),
            "pm": round(df["price"].mean(), 2)
        }

dados = pd.DataFrame(dados, columns=[
    "nome", "tipo", "segmento", "cotacao", "pvp",  "quantidade", "pm"])

_, fiis_category, fiis_names = load_fiis(
    st.session_state["user"]["_id"])

dados["categoria"] = dados["nome"].map(fiis_category)

dados["saldo"] = dados["quantidade"] * dados["cotacao"]
dados["valor investido"] = dados["quantidade"] * dados["pm"]

dados["ganho percentual"] = (
    (dados["saldo"] / dados["valor investido"])-1)*100
dados["ganho saldo"] = dados["saldo"] - dados["valor investido"]

infos = dados[["nome", "segmento", "tipo", "quantidade", "pm", "valor investido", "cotacao",
               "ganho percentual", "ganho saldo", "saldo", "pvp", "categoria"]]

infos.rename(columns={
    "nome": "Ativo",
    "segmento": "Segmento",
    "tipo": "Tipo",
    "quantidade": "Quantidade",
    "cotacao": "Preço Atual",
    "saldo": "Saldo",
    "pvp": "P/VP",
    "pm": "Preço Médio",
    "ganho saldo": "Ganho",
    "ganho percentual": "% Ganho",
    "valor investido": "Valor Investido",
    "categoria": "Categoria"
}, inplace=True)

infos.sort_values(by=["Saldo"], inplace=True, ascending=False)

total = infos["Saldo"].sum()

infos["Percentual"] = (infos["Saldo"] / total) * 100

resume(infos, columns=[
    "Ativo",
    "Segmento",
    "Tipo",
    "Quantidade",
    "Preço Médio",
    "Valor Investido",
    "Preço Atual",
    "Saldo",
    "% Ganho",
    "Ganho",
    "P/VP",
    "Categoria",
    "Percentual"
])

graphics(infos)

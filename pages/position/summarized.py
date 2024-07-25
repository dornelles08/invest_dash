import calendar
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from components.resume import resume
from functions.load_data import load_fiis
from services.dados import DadosService
from services.price_mouth import PriceMonthService
from services.transaction import TransactionsService
from services.unfolding import UnfoldingService


def convert_date(data_str):
    return datetime.strptime(data_str, "%m/%Y")


def last_day_month(data_str):
    date = datetime.strptime(data_str, "%m/%Y")
    last_day = calendar.monthrange(date.year, date.month)[1]
    return datetime(date.year, date.month, last_day)


transaction_service = TransactionsService()
dados_service = DadosService()
price_month_service = PriceMonthService()
unfoldin_service = UnfoldingService()

transactions = transaction_service.get_transactions(
    st.session_state["user"]["_id"], order_by="date")

ativos = transaction_service.get_fiis_from_transactions(
    st.session_state["user"]["_id"])

prices_months = price_month_service.get_by_ativos(ativos)

dates = [t["date"].strftime("%m/%Y") for t in transactions]
dates = list(set(dates))

dates.sort(key=convert_date, reverse=True)

col, _ = st.columns([5, 10])
ref = col.selectbox("Referência", dates)

st.header(f"Posição em {ref}", divider=True)

ref_date = last_day_month(ref)

filtered_transactions = list(
    filter(lambda x: x["date"] < ref_date, transactions))

filtered_transactions = pd.DataFrame(filtered_transactions, columns=[
    '_id', 'ativo', 'qtd', 'price', 'date', 'total', 'user_id'])

transactions_groups = filtered_transactions.groupby("ativo")
fiis = [ativo for ativo, _ in transactions_groups]

dados = dados_service.get_dados(fiis)
for ativo, df in transactions_groups:
    unfolding_ativo = unfoldin_service.get_by_ativo(ativo)

    indice = next((index for (index, d) in enumerate(
        dados) if d["nome"] == ativo), None)

    ativo_price_month = list(
        filter(lambda x: x["ativo"] == ativo, prices_months))[0]

    price_month = list(filter(
        lambda x: f"{x['mes']}/{x['ano']}" == ref,
        ativo_price_month["price_month"]
    ))[0]

    cotacao = float(price_month["close"])

    if unfolding_ativo is not None:
        unfolding_date = last_day_month(
            unfolding_ativo["mes"]+"/"+unfolding_ativo["ano"])

        if unfolding_date > ref_date:
            cotacao = cotacao/10

    if indice is not None:
        dados[indice] = {
            **dados[indice],
            "cotacao": cotacao,
            "quantidade": df["qtd"].sum(),
            "pm": round(df["price"].mean(), 2)
        }


dados = pd.DataFrame(dados, columns=[
    "nome", "cotacao", "pvp",  "quantidade", "pm"])

_, fiis_category, fiis_names = load_fiis(
    st.session_state["user"]["_id"])

dados["categoria"] = dados["nome"].map(fiis_category)

dados["saldo"] = dados["quantidade"] * dados["cotacao"]
dados["valor investido"] = dados["quantidade"] * dados["pm"]

dados["ganho percentual"] = (
    (dados["saldo"] / dados["valor investido"])-1)*100
dados["ganho saldo"] = dados["saldo"] - dados["valor investido"]

infos = dados[["nome", "quantidade", "pm", "valor investido", "cotacao",
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

infos.sort_values(by=["Ganho"], inplace=True, ascending=False)

total = infos["Saldo"].sum()

infos["Percentual"] = (infos["Saldo"] / total) * 100

col1, col2 = st.columns([1, 1])

fig = go.Figure()

positive_infos = infos[infos["Ganho"] >= 0]
positive_infos = positive_infos.sort_values(by=["Ganho"], ascending=True)

negative_infos = infos[infos["Ganho"] < 0]
negative_infos = negative_infos.sort_values(by=["Ganho"], ascending=True)

fig.add_trace(
    go.Bar(y=negative_infos["Ativo"], x=negative_infos["Ganho"],
           orientation='h', marker_color="red"))
fig.add_trace(
    go.Bar(y=positive_infos["Ativo"], x=positive_infos["Ganho"],
           orientation='h', marker_color="green"))
fig.update_layout(showlegend=False)

col1.plotly_chart(fig, use_container_width=True)

resume_general = pd.DataFrame({
    "Total de Ativos": [infos["Ganho"].count()],
    "Ganhos Totais": [round(infos["Ganho"].sum(), 2)],
    "Ganhos Percentuais": [round(infos["% Ganho"].sum(), 2)],
})
col1.dataframe(data=resume_general,
               hide_index=True,
               column_config={
                   "Ganhos Percentuais": st.column_config.NumberColumn(format="%.2f %%"),
                   "Ganhos Totais": st.column_config.NumberColumn(format="R$ %.2f"),
               })

resume(infos, columns=[
    "Ativo",
    "Preço Atual",
    "Ganho",
    "% Ganho"
], display=col2)

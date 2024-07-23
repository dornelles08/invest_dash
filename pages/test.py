from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from functions.configs import valid_user_logged
from services.dados import DadosService
from services.price_mouth import PriceMonthService
from services.transaction import TransactionsService

price_month_service = PriceMonthService()
transaction_service = TransactionsService()

fiis = transaction_service.get_fiis_from_transactions(
    st.session_state["user"]["_id"])

prices_fiis = []

for fii in fiis:
    prices = price_month_service.get_by_ativo(fii)
    if prices:
        for price in prices["price_month"]:
            if float(price["close"]) < 10000:
                prices_fiis.append({
                    "ativo": fii,
                    **price
                })


prices_fiis = pd.DataFrame(prices_fiis)

prices_fiis["mesAno"] = prices_fiis["mes"] + "/" + prices_fiis["ano"]
prices_fiis["mesAno"] = pd.to_datetime(
    prices_fiis["mesAno"], format="%m/%Y") + pd.offsets.MonthEnd(0)

prices_fiis

mes_ano = "02/2024"
mes_ano = pd.to_datetime(
    mes_ano, format='%m/%Y') + pd.offsets.MonthEnd(0)

transactions = transaction_service.get_transactions(st.session_state["user"]["_id"], {
    "date": {"$lte": mes_ano},
    "ativo": {"$in":  list(prices_fiis["ativo"].unique())}
})

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

transactions

mes_ano

prices_fiis_mes_ano = prices_fiis[prices_fiis["mesAno"] == mes_ano][[
    "ativo", "close"]]

st.dataframe(prices_fiis_mes_ano)

resultado = transactions.groupby('ativo')['Saldo'].sum().reset_index()

# prices_group = prices_fiis.groupby(by="ativo")

# for ativo, group in prices_group:
#     st.dataframe(group)

# fig = go.Figure()
# ativos = prices_fiis["ativo"].unique()
# for ativo in ativos:
#     df_ativo = prices_fiis[prices_fiis["ativo"] == ativo]
#     fig.add_trace(go.Scatter(
#         x=df_ativo["mesAno"], y=df_ativo["close"], mode="lines", name=ativo))

# fig.update_layout(
#     title="Preço de Fechamento por Ativo ao Longo do Tempo",
#     xaxis_title="Data",
#     yaxis_title="Preço de Fechamento",
#     legend_title="Ativos"
# )

# st.plotly_chart(fig, use_container_width=True)

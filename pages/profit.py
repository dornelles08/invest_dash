import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from functions.configs import valid_user_logged
from functions.utils import last_day_month
from services.price_mouth import PriceMonthService
from services.transaction import TransactionsService
from services.unfolding import UnfoldingService

valid_user_logged()


def find_price_month(row, prices_months_, mes_ano):
    ativo_name = row['Ativo']
    ano = int(mes_ano.split("-")[0])
    mes = int(mes_ano.split("-")[1])
    price_month_ativo = list(
        filter(lambda x: x["ativo"] == ativo_name, prices_months_))[0]["price_month"]

    price_month = list(filter(lambda x: int(x["ano"]) ==
                              ano and int(x["mes"]) == mes, price_month_ativo))

    price_month = price_month[0]
    cotacao = float(price_month["close"])

    unfolding_ativo = unfoldin_service.get_by_ativo(ativo_name)
    if unfolding_ativo is not None:
        unfolding_date = last_day_month(
            unfolding_ativo["mes"]+"/"+unfolding_ativo["ano"])

        if unfolding_date > last_day_month(f"{mes}/{ano}"):
            cotacao = cotacao/10

    return cotacao


def get_month_profit(mes_ano):
    transactions_filtered = transactions[transactions["Data"]
                                         <= mes_ano["Data"]]

    transactions_filtered["preço mes referencia"] = transactions_filtered.apply(
        lambda row: find_price_month(row, prices_months, mes_ano["Data"]), axis=1)

    transactions_filtered["rentabilidade"] = transactions_filtered["preço mes referencia"] - \
        transactions["Preço"]

    transactions_filtered["Rentabilidade"] = transactions_filtered["rentabilidade"] * \
        transactions["Quantidade"]

    return transactions_filtered["Rentabilidade"].sum()


transaction_service = TransactionsService()
price_month_service = PriceMonthService()
unfoldin_service = UnfoldingService()

st.header("Rentabilidade", divider=True)

transactions = transaction_service.get_transactions(
    st.session_state["user"]["_id"], order_by="date")

transactions = pd.DataFrame(transactions, columns=[
                            "ativo", "qtd", "price", "date", "total"])

transactions.rename(columns={
    "ativo": "Ativo",
    "qtd": "Quantidade",
    "price": "Preço",
    "total": "Total",
    "date": "Data da Compra",
}, inplace=True)

transactions["Data da Compra"] = pd.to_datetime(
    transactions["Data da Compra"], format="%d/%m/%y")

transactions["Data"] = transactions["Data da Compra"].dt.to_period("M")

transactions.sort_values(by="Data da Compra", ascending=True)

fiis_names = transaction_service.get_fiis_from_transactions(
    st.session_state["user"]["_id"])


col1, _ = st.columns([1, 1])
ativo = col1.selectbox("Fii", fiis_names, index=None)

if ativo:
    transactions = transactions[transactions["Ativo"] == ativo]

group_transactions_mes_ano = transactions.groupby(
    "Data")["Total"].sum().reset_index()

group_transactions_mes_ano.rename(columns={
    "Total": "Compras"
}, inplace=True)

# Grafico Total Investido por Mês
group_transactions_mes_ano["Data"] = group_transactions_mes_ano["Data"].astype(
    str)

st.subheader("Total Investido por Mês")
fig = go.Figure(
    data=[go.Bar(x=group_transactions_mes_ano["Data"], y=group_transactions_mes_ano["Compras"])])
fig.update_layout(
    xaxis_title="Mês",
    yaxis_title="Valor Investido",
    barmode="group"
)
st.plotly_chart(fig)

# Grafico Total Investido Acumulado Mês a Mês
group_transactions_mes_ano["Patrimônio"] = group_transactions_mes_ano["Compras"].cumsum(
)

st.subheader("Total Investido")
fig = go.Figure(
    data=[go.Bar(x=group_transactions_mes_ano["Data"],
                 y=group_transactions_mes_ano["Patrimônio"])])
fig.update_layout(
    xaxis_title="Mês",
    yaxis_title="Total",
    barmode="group"
)
st.plotly_chart(fig)


# Grafico Total Investido Acumulado Mês a Mês - Resultado
prices_months = price_month_service.get_by_ativos(fiis_names)

group_transactions_mes_ano["Rentabilidade"] = group_transactions_mes_ano.apply(
    get_month_profit, axis=1)

st.subheader("Rentabilidade Mensal")
fig = go.Figure()
fig.add_trace(go.Bar(name='Rentabilidade',
                     x=group_transactions_mes_ano["Data"],
                     y=group_transactions_mes_ano["Rentabilidade"]))

fig.update_layout(
    xaxis_title="Mês",
    yaxis_title="Total",
    barmode="stack"
)

st.plotly_chart(fig, use_container_width=True)

group_transactions_mes_ano["Saldo"] = group_transactions_mes_ano["Patrimônio"] + \
    group_transactions_mes_ano["Rentabilidade"]
group_transactions_mes_ano["% Rentabilidade"] = ((group_transactions_mes_ano["Saldo"] /
                                                  group_transactions_mes_ano["Patrimônio"])-1)*100

st.dataframe(
    data=group_transactions_mes_ano,
    hide_index=True,
    use_container_width=True,
    height=500,
    column_config={
        "Compras": st.column_config.NumberColumn(format="R$ %.2f"),
        "Patrimônio": st.column_config.NumberColumn(format="R$ %.2f"),
        "Rentabilidade": st.column_config.NumberColumn(format="R$ %.2f"),
        "Saldo": st.column_config.NumberColumn(format="R$ %.2f"),
        "% Rentabilidade": st.column_config.NumberColumn(format="%.2f %%"),
    }
)

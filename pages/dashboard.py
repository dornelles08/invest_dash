from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from functions.configs import valid_user_logged
from functions.load_data import get_fiis_infos, load_fiis
from services.dados import DadosService
from services.transaction import TransactionsService
from services.user import UserService

st.set_page_config(
    layout="wide",
)

valid_user_logged()

transaction_service = TransactionsService()
dados_service = DadosService()
user_services = UserService()

if "dados" not in st.session_state or st.session_state["dados"] is None:
    transactions = transaction_service.get_transactions(
        st.session_state["user"]["_id"])

    transactions = pd.DataFrame(transactions, columns=[
                                '_id', 'ativo', 'qtd', 'price', 'date', 'total', 'user_id'])

    transactions = transactions[["ativo", "qtd", "price", "date", "total"]]

    transactions_groups = transactions.groupby("ativo")
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
    dados["valorização"] = ((dados["cotacao"] / dados["pm"])-1)*100

    infos = dados[["nome", "segmento", "tipo", "quantidade", "pm", "cotacao", "valorização",
                   "saldo", "pvp", "categoria"]]

    infos.rename(columns={
        "nome": "Ativo",
        "segmento": "Segmento",
        "tipo": "Tipo",
        "quantidade": "Quantidade",
        "cotacao": "Preço Atual",
        "saldo": "Saldo",
        "pvp": "P/VP",
        "pm": "Preço Médio",
        "valorização": "Valorização",
        "categoria": "Categoria"
    }, inplace=True)

    infos.sort_values(by=["Saldo"], inplace=True, ascending=False)

    total = infos["Saldo"].sum()

    infos["Percentual"] = (infos["Saldo"] / total) * 100

    st.session_state["dados"] = infos
else:
    infos = st.session_state["dados"]

# Title
st.title("Carteira Fundos Imobiliários")

# Cards
investido = round((infos["Quantidade"]*infos["Preço Médio"]).sum(), 2)
saldo_total = round(infos["Saldo"].sum(), 2)
variation = round(((saldo_total/investido)-1)*100, 2)

col1, _, col2 = st.columns([8, 1, 1], vertical_alignment="bottom")
col1.metric(label="Total Investido", value=f"R$ {
            saldo_total}", delta=f"{variation} %")

if col2.button("Atualizar Base"):
    user_sync = datetime.strptime(st.session_state["user"]["sync"], "%x %X")
    if (user_sync - datetime.now()).seconds >= 900:
        fiis_infos = get_fiis_infos(st, st.session_state["user"]["_id"])
        dados_service.upsert_dados(fiis_infos)
        user_services.update_user({
            **st.session_state["user"],
            "sync": datetime.now().strftime("%x %X")
        })
    st.session_state["dados"] = None
    st.success("Transação Adicionada com Sucesso", icon="✅")
    st.rerun()

st.divider()

# Listagem
st.title("Ativos")
st.dataframe(infos, hide_index=True, height=500, use_container_width=True, column_config={
    "Preço Atual": st.column_config.NumberColumn(format="R$ %.2f"),
    "Preço Médio": st.column_config.NumberColumn(format="R$ %.2f"),
    "Saldo": st.column_config.NumberColumn(format="R$ %.2f"),
    "Percentual": st.column_config.NumberColumn(format="%.2f %%"),
    "Valorização": st.column_config.NumberColumn(format="%.2f %%"),
})
st.divider()

# Graficos
st.title("Gráficos")


def make_graphics(tab, subheader, result, column):
    container = tab.container(border=True)
    container.subheader(subheader)
    coluna1, coluna2 = container.columns([1, 3])

    result["Porcentagem"] = (result["Saldo"] / result["Saldo"].sum()) * 100
    result.sort_values(by=["Porcentagem"], inplace=True, ascending=False)

    coluna1.dataframe(result[[column, "Porcentagem"]],
                      hide_index=True, height=500, use_container_width=True,
                      column_config={"Porcentagem": st.column_config.NumberColumn(format="%.2f %%"),
                                     })
    fig = go.Figure(
        data=[go.Pie(labels=result[column], values=result["Saldo"])])
    coluna2.plotly_chart(fig, use_container_width=True)


tab1, tab2, tab3, tab4 = st.tabs(
    ["Categorias", "Ativos", "Segmentos", "Tipos"])

resultado = infos.groupby('Categoria')['Saldo'].sum().reset_index()
make_graphics(tab1, "Categorias", resultado, "Categoria")

resultado = infos.copy()
make_graphics(tab2, "Ativos", resultado, "Ativo")

resultado = infos.groupby('Segmento')['Saldo'].sum().reset_index()
make_graphics(tab3, "Segmentos", resultado, "Segmento")

resultado = infos.groupby('Tipo')['Saldo'].sum().reset_index()
make_graphics(tab4, "Tipos", resultado, "Tipo")

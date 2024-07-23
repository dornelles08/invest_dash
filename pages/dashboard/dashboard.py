import pandas as pd
import streamlit as st

from functions.configs import valid_user_logged
from functions.load_data import load_fiis
from pages.dashboard.cards import cards
# from pages.dashboard.graphics import graphics
from pages.dashboard.resume import resume
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

    st.session_state["dados"] = infos
else:
    infos = st.session_state["dados"]

# Title
st.header("Carteira Fundos Imobiliários", divider=True)

# Cards
cards(infos)

# Resumo
resume(infos)

# Graficos
# graphics(infos)

import plotly.graph_objects as go
import streamlit as st

from functions.load_data import load_data, load_fiis

st.set_page_config(
    layout="wide",
)

if "dados" not in st.session_state:
    dados = load_data()
    st.session_state["dados"] = dados

dados = st.session_state["dados"]

fiis, fiis_category, fiis_names, fiis_qtd = load_fiis()

dados["quantidade"] = dados["nome"].map(fiis_qtd)
dados["categoria"] = dados["nome"].map(fiis_category)
dados["saldo"] = dados["quantidade"] * dados["cotacao"]

infos = dados[["nome", "segmento", "tipo", "quantidade",
               "cotacao", "saldo", "pvp", "categoria"]]
infos = infos.rename(columns={
    "nome": "Ativo",
    "segmento": "Segmento",
    "tipo": "Tipo",
    "quantidade": "Quantidade",
    "cotacao": "Preço Atual",
    "saldo": "Saldo",
    "pvp": "P/VP",
    "categoria": "Categoria"
})
infos.sort_values(by=["Tipo", "Segmento"], inplace=True)

st.dataframe(infos, hide_index=True, height=500, use_container_width=True, column_config={
    "Preço Atual": st.column_config.NumberColumn(format="R$ %f"),
    "Saldo": st.column_config.NumberColumn(format="R$ %f")
})

col1, col2 = st.columns([1, 1])

resultado = infos.groupby('Categoria')['Saldo'].sum().reset_index()
fig = go.Figure(
    data=[go.Pie(labels=resultado["Categoria"], values=resultado["Saldo"])])
col1.plotly_chart(fig, use_container_width=True)

fig = go.Figure(
    data=[go.Pie(labels=infos["Ativo"], values=infos["Saldo"])])
col2.plotly_chart(fig, use_container_width=True)

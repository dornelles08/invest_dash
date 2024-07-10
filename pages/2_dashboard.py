import plotly.graph_objects as go
import streamlit as st

from functions.load_data import load_data, load_fiis

st.set_page_config(
    layout="wide",
)

if "token" not in st.session_state or st.session_state.token is None or "user" not in st.session_state or st.session_state.user is None:
    st.session_state["token"] = None
    st.session_state["user"] = None
    st.switch_page("1_home.py")

if "dados" not in st.session_state or st.session_state["dados"] is None:
    fiis, fiis_category, fiis_names, fiis_qtd = load_fiis(
        st.session_state["user"]["_id"])
    dados = load_data(fiis_names)
    st.session_state["dados"] = dados

sair_button = st.button("Sair")
if sair_button:
    st.session_state["token"] = None
    st.session_state["user"] = None
    st.switch_page("1_home.py")

dados = st.session_state["dados"]

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

total = infos["Saldo"].sum()

infos["Percentual"] = (infos["Saldo"] / total) * 100

st.title(f"Total Investido - R$ {round(total, 2)}")
st.divider()

# Listagem
st.title("Ativos")
st.dataframe(infos, hide_index=True, height=500, use_container_width=True, column_config={
    "Preço Atual": st.column_config.NumberColumn(format="R$ %.2f"),
    "Saldo": st.column_config.NumberColumn(format="R$ %.2f"),
    "Percentual": st.column_config.NumberColumn(format="%.2f %%"),
})
st.divider()

# Graficos
st.title("Gráficos")
col1, col2 = st.columns([1, 1])

resultado = infos.groupby('Categoria')['Saldo'].sum().reset_index()
fig = go.Figure(
    data=[go.Pie(labels=resultado["Categoria"], values=resultado["Saldo"])])
col1.plotly_chart(fig, use_container_width=True)

fig = go.Figure(
    data=[go.Pie(labels=infos["Ativo"], values=infos["Saldo"])])
col2.plotly_chart(fig, use_container_width=True)

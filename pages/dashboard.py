import plotly.graph_objects as go
import streamlit as st

from functions.load_data import load_data, load_fiis

st.set_page_config(
    layout="wide",
)

if "token" not in st.session_state or st.session_state.token is None or \
        "user" not in st.session_state or st.session_state.user is None:
    st.session_state["token"] = None
    st.session_state["user"] = None
    st.switch_page("home.py")

if "dados" not in st.session_state or st.session_state["dados"] is None:
    _, _, fiis_names, _ = load_fiis(
        st.session_state["user"]["_id"])
    dados = load_data(fiis_names)
    st.session_state["dados"] = dados

dados = st.session_state["dados"]

_, fiis_category, _, fiis_qtd = load_fiis(
    st.session_state["user"]["_id"])

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


def make_graphics(tab, subheader, result, column):
    container = tab.container(border=True)
    container.subheader(subheader)
    col1, col2 = container.columns([1, 3])
    col1.dataframe(result[[column, "Saldo"]],
                   hide_index=True, height=500, use_container_width=True,
                   column_config={"Saldo": st.column_config.NumberColumn(format="R$ %.2f"),
                                  })
    fig = go.Figure(
        data=[go.Pie(labels=result[column], values=result["Saldo"])])
    col2.plotly_chart(fig, use_container_width=True)


tab1, tab2, tab3, tab4 = st.tabs(
    ["Categorias", "Ativos", "Segmentos", "Tipos"])

resultado = infos.groupby('Categoria')['Saldo'].sum().reset_index()
make_graphics(tab1, "Categorias", resultado, "Categoria")

make_graphics(tab2, "Ativos", infos, "Ativo")

resultado = infos.groupby('Segmento')['Saldo'].sum().reset_index()
make_graphics(tab3, "Segmentos", resultado, "Segmento")

resultado = infos.groupby('Tipo')['Saldo'].sum().reset_index()
make_graphics(tab4, "Tipos", resultado, "Tipo")

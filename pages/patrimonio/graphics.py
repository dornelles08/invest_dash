import plotly.graph_objects as go
import streamlit as st


def make_graphics(tab, subheader, result, column):
    """ 
      Monta o grafico com base no df e na coluna passado por parametro
    """
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


def graphics(infos):
    """   
      Cria graficos para 4 agrupamentos
      Categorias, Ativos, Segmentos, Tipos
    """
    st.title("Gráficos")
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

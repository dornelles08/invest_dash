import pandas as pd
import streamlit as st


def ajustar_colunas(df, columns):
    for column in columns:
        df[column] = df[column].str.replace(
            'R$', '', regex=False).str.replace('.', '').str.replace(',', '.').astype(float)

    return df


col1, col2 = st.columns([1, 1])

proventos = col1.file_uploader("Planilha de Proventos", type="csv")
rentabilidade = col2.file_uploader("Planilha de Rentabilidade", type="csv")

if proventos is not None and rentabilidade is not None:
    proventos_bytes_data = proventos.read()
    with open("data/proventos.csv", "w", encoding="utf-8") as arq:
        arq.write(proventos_bytes_data.decode("utf-8"))

    rentabilidade_bytes_data = rentabilidade.read()
    with open("data/rentabilidade.csv", "w", encoding="utf-8") as arq:
        arq.write(rentabilidade_bytes_data.decode("utf-8"))

    proventos = pd.read_csv("data/proventos.csv")
    rentabilidade = pd.read_csv("data/rentabilidade.csv")
    rentabilidade.drop(rentabilidade.index[-1], inplace=True)

    proventos = ajustar_colunas(
        proventos.copy(), ["Recebido", "Preço médio", "Cotação", "Valor por cota"])
    proventos_soma = proventos.groupby('Ativo')['Recebido'].sum().reset_index()
    proventos_soma.rename(columns={'Recebido': 'Dividendos'}, inplace=True)

    rentabilidade = ajustar_colunas(
        rentabilidade.copy(), ["Preço médio", "Preço atual"])
    rentabilidade["Total investido"] = rentabilidade["Qtd"] * \
        rentabilidade["Preço médio"]
    rentabilidade["Total atual"] = rentabilidade["Qtd"] * \
        rentabilidade["Preço atual"]
    rentabilidade["Ganho"] = rentabilidade["Total atual"] - \
        rentabilidade["Total investido"]
    rentabilidade["% Ganho"] = ((rentabilidade["Total atual"] /
                                rentabilidade["Total investido"])-1)*100
    rentabilidade = pd.merge(
        rentabilidade, proventos_soma, on='Ativo', how='left')
    rentabilidade["Ganho Real"] = rentabilidade["Ganho"] + \
        rentabilidade["Dividendos"]

    ganho_total = rentabilidade["Ganho Real"].sum()
    total_investido = rentabilidade["Total investido"].sum()

    ganho_percentual = ganho_total/total_investido

    st.metric(label="Ganho Real Total", value=f"R$ {round(ganho_total,2)}")

    st.dataframe(data=rentabilidade, height=500, column_config={
        "Preço médio": st.column_config.NumberColumn(format="R$ %.2f"),
        "Total investido": st.column_config.NumberColumn(format="R$ %.2f"),
        "Preço atual": st.column_config.NumberColumn(format="R$ %.2f"),
        "Total atual": st.column_config.NumberColumn(format="R$ %.2f"),
        "Ganho": st.column_config.NumberColumn(format="R$ %.2f"),
        "Dividendos": st.column_config.NumberColumn(format="R$ %.2f"),
        "Ganho Real": st.column_config.NumberColumn(format="R$ %.2f"),
        "% Ganho": st.column_config.NumberColumn(format="%.2f %%"),
    })

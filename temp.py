import pandas as pd

from functions.load_data import load_data, load_fiis_category, load_fiis_qtd

dados = load_data()

fiis_qtd = load_fiis_qtd()
fiis_category = load_fiis_category()

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

resultado = infos.groupby('Categoria')['Saldo'].sum().reset_index()

print(resultado)

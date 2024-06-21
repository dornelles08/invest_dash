import json

import pandas as pd
import streamlit as st

from functions.get_fii_details import get_fii
from functions.load_data import get_fiis_infos, load_data, load_fiis

st.header("Atualizar informações sobre oa Ativos", divider=True)

if st.button("Atualizar Base"):
    fiis_infos = get_fiis_infos(st)
    pd.DataFrame(data=fiis_infos).to_csv("data/data.csv", index=False)
    st.write("Informações atualizadas")


st.header("Adicionar Novo Ativo", divider=True)
col1, col2, col3 = st.columns([1, 1, 1])
new_ativo = col1.text_input("Nome do Novo Ativo")
new_qtd_ativo = col2.number_input(
    "Quantidade do Novo Ativo",  value=None, min_value=0)
new_category_ativo = col3.text_input("Categoria do Novo Ativo")

if st.button("Adicionar Ativo"):
    data = load_data()
    fii_infos = get_fii(new_ativo)
    fii_infos = pd.DataFrame(data=[fii_infos])
    new_data = pd.concat([data, fii_infos], ignore_index=True)
    new_data.to_csv("../data/data.csv", index=False)

    fiis, _, _, _ = load_fiis()
    with open("data/fiis.json", "w", encoding="utf-8") as file:
        fiis.append({
            "ativo": new_ativo,
            "qtd": new_qtd_ativo,
            "category": new_category_ativo
        })
        json.dump(fiis, file)
        st.write("Ativo adicionado")


st.header("Atualizar Quantidade de um Ativo", divider=True)
_, fiis_category, fiis_names, fiis_qtd = load_fiis()
col1, col2, col3 = st.columns([1, 1, 1])
ativo = col1.selectbox("Fii", fiis_names)
qtd_ativo = col2.number_input(
    "Quantidade do Ativo",  value=fiis_qtd[ativo], min_value=0)
category_ativo = col3.text_input("Categoria do Ativo", fiis_category[ativo])

if st.button("Atualizar Ativo"):
    fiis, _, _, _ = load_fiis()
    with open("data/fiis.json", "w", encoding="utf-8") as file:
        fiis.append({
            "ativo": ativo,
            "qtd": qtd_ativo,
            "category": category_ativo
        })
        json.dump(fiis, file)
        st.write("Ativo atualizado")

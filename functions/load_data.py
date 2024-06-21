import json

import pandas as pd

from functions.get_fii_details import get_fii


def load_fiis():
    """
        Busca todas informações de Fiis
    """
    with open("data/fiis.json", "r", encoding="utf-8") as file:
        fiis = json.load(file)

    fiis_category = {}
    for fii in fiis:
        fiis_category[fii["ativo"]] = fii["category"]

    fiis_names = []
    for fii in fiis:
        fiis_names.append(fii["ativo"])

    fiis_qtd = {}
    for fii in fiis:
        fiis_qtd[fii["ativo"]] = fii["qtd"]

    return fiis, fiis_category, fiis_names, fiis_qtd


def get_fiis_infos(st):
    """
        Busca os informações dos Fiis
    """
    bar = st.progress(0, text="Buscando Informações Atualizadas")
    _, _, fiis, _ = load_fiis()
    fiis_details = []
    for i, fii in enumerate(fiis):
        percent = i/(len(fiis)-1)

        bar.progress(percent, text=fii)
        data = get_fii(fii)
        # data = {
        #     "fii": fii
        # }
        fiis_details.append(data)

    return fiis_details


def load_data():
    return pd.read_csv("data/data.csv")

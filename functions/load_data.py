import json

import pandas as pd

from functions.get_fii_details import get_fii
from services.dados import DadosService
from services.fiis import FiisService


def load_fiis():
    """
        Busca todas informações de Fiis
    """
    fiis_service = FiisService()
    fiis = fiis_service.get_fiis()

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
        fiis_details.append(data)

    return fiis_details


def load_data():
    dados_service = DadosService()
    dados = dados_service.get_dados()
    return pd.DataFrame(dados, columns=["nome", "tipo", "segmento", "vacancia", "cotacao", "valorizacao_diaria", "valorizacao_mensal", "valorizacao_anual", "dy", "ultimos_12_dividendos", "pvp", "ultimo_dividendo", "ultimo_rendimento", "ultima_cotacao_base", "ultima_data_com", "ultima_data_pagamento", "proximo_dividendo", "proximo_rendimento", "proxima_cotacao_base", "proxima_data_com", "proxima_data_pagamento"])

from services.dados import DadosService

dados_service = DadosService()

dados_service.upsert_dado({
    "nome": "HSML11",
    "tipo": "Fundo de Tijolo",
    "segmento": "Shoppings / Varejo",
    "vacancia": 4.9,
    "cotacao": 93.05,
    "valorizacao_diaria": 1.11,
    "valorizacao_mensal": -1.5,
    "valorizacao_anual": 0.26,
    "dy": 9.91,
    "ultimos_12_dividendos": 9.22,
    "pvp": 0.97,
    "ultimo_dividendo": 0.8,
    "ultimo_rendimento": 0.8218,
    "ultima_cotacao_base": 97.35,
    "ultima_data_com": "28/06/2024",
    "ultima_data_pagamento": "05/07/2024",
    "proximo_dividendo": "-",
    "proximo_rendimento": "-",
    "proxima_cotacao_base": "-",
    "proxima_data_com": "-",
    "proxima_data_pagamento": "-"
})

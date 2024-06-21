import requests
from bs4 import BeautifulSoup


def get_html(url):
    html = requests.get(url, headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }, timeout=5000)

    html = BeautifulSoup(html.text, "html.parser")

    return html


def convert_string_to_float(price):
    return float(price.replace("R$ ", "").replace("%", "").replace(".", "").replace(",", "."))


def get_card_information(html_doc, card):
    return convert_string_to_float(html_doc.find(class_=card).find(
        class_="_card-body").find("span").get_text())


def get_investidor10_infos(fii):
    try:
        url = f"https://investidor10.com.br/fiis/{fii}"

        html = get_html(url)

        nome = html.find(
            class_='name-ticker').get_text().replace("\n", " ").strip()

        cotacao = get_card_information(html, "cotacao")
        dy = get_card_information(html, "dy")
        pvp = get_card_information(html, 'vp')

        indicadores = html.find(id='table-indicators').find_all(class_='cell')
        principais_indicadores = ['TIPO DE FUNDO',
                                  'SEGMENTO', 'ÚLTIMO RENDIMENTO', 'VACÂNCIA']
        indicadores_selecionados = {}
        for indicador in indicadores:
            if indicador.find(class_='desc').find('span').get_text().strip() in principais_indicadores:
                if indicador.find(class_='desc').find('span').get_text().strip() == "ÚLTIMO RENDIMENTO":
                    indicadores_selecionados[indicador.find(class_='desc').find('span').get_text(
                    ).strip()] = convert_string_to_float(indicador.find(class_='desc').find(class_='value').get_text().strip())
                else:
                    indicadores_selecionados[indicador.find(class_='desc').find('span').get_text(
                    ).strip()] = indicador.find(class_='desc').find(class_='value').get_text().strip()

        return {
            "nome": nome,
            "cotacao": cotacao,
            "dy": dy,
            "pvp": pvp,
            **indicadores_selecionados
        }
    except Exception as e:
        print(e)


def is_fiagro(fii):
    fiagros = ['VGIA11']
    if fii in fiagros:
        return True
    return False


def convert_to_float(string):
    try:
        return float(string.replace(".", "").replace(",", ".").replace("%", "").replace("R$ ", ""))
    except Exception as _:
        return string


def get_fii(fii):
    try:
        url = f"https://statusinvest.com.br/fundos-imobiliarios/{fii}"
        if is_fiagro(fii):
            url = f"https://statusinvest.com.br/fiagros/{fii}"

        html = get_html(url)
        
        nome = html.find("h1").get_text()

        cotacao = convert_to_float(html.find(title="Valor atual do ativo").find(
            "strong").get_text())

        valorizacao_diaria = convert_to_float(html.find(
            title="Variação do valor do ativo com base no dia anterior").find("b").get_text())

        valorizacao_mensal = convert_to_float(html.find(
            title="Valorização no preço do ativo com base no mês atual").find("b").get_text())

        valorizacao_anual = convert_to_float(html.find(
            title="Valorização no preço do ativo com base nos últimos 12 meses").find("strong").get_text())

        dy = convert_to_float(html.find(
            title="Dividend Yield com base nos últimos 12 meses").find("strong").get_text())

        ultimos_12_dividendos = convert_to_float(html.find(
            title="Soma total de proventos distribuídos nos últimos 12 meses").find(class_="sub-value").get_text())

        pvp = convert_to_float(html.find_all(class_='top-info')[1].find_all(class_='info')[1].find(
            'strong').get_text())

        ultimo_rendimento = html.find(id="dy-info").find(class_="info")
        ultimo = {
            "ultimo_dividendo": convert_to_float(ultimo_rendimento.find('strong').get_text()),
            "ultimo_rendimento": convert_to_float(ultimo_rendimento.find_all('div')[1].find_all(class_='sub-info')[0].find('b').get_text()),
            "ultima_cotacao_base": convert_to_float(ultimo_rendimento.find_all('div')[1].find_all(class_='sub-info')[1].find('b').get_text()),
            "ultima_data_com": ultimo_rendimento.find_all('div')[1].find_all(class_='sub-info')[2].find('b').get_text(),
            "ultima_data_pagamento": ultimo_rendimento.find_all('div')[1].find_all(class_='sub-info')[3].find('b').get_text(),
        }

        proximo_rendimento = html.find(id="dy-info").find_next_sibling()
        proximo = {
            "proximo_dividendo": convert_to_float(proximo_rendimento.find(class_="info").find('strong').get_text()),
            "proximo_rendimento": convert_to_float(proximo_rendimento.find(class_="info").find_all('div')[1].find_all(class_='sub-info')[0].find('b').get_text()),
            "proxima_cotacao_base": convert_to_float(proximo_rendimento.find(class_="info").find_all('div')[1].find_all(class_='sub-info')[1].find('b').get_text()),
            "proxima_data_com": proximo_rendimento.find(class_="info").find_all('div')[1].find_all(class_='sub-info')[2].find('b').get_text(),
            "proxima_data_pagamento": proximo_rendimento.find(class_="info").find_all('div')[1].find_all(class_='sub-info')[3].find('b').get_text(),
        }

        investidor10_response = get_investidor10_infos(fii)

        return {
            "nome": nome.split('-')[0].strip(),
            "tipo": investidor10_response["TIPO DE FUNDO"],
            "segmento": investidor10_response["SEGMENTO"],
            "vacancia": convert_to_float(investidor10_response["VACÂNCIA"]),
            "cotacao": cotacao,
            "valorizacao_diaria": valorizacao_diaria,
            "valorizacao_mensal": valorizacao_mensal,
            "valorizacao_anual": valorizacao_anual,
            "dy": dy,
            "ultimos_12_dividendos": ultimos_12_dividendos,
            "pvp": pvp,
            **ultimo,
            **proximo,
        }
    except Exception as e:
        print(e)

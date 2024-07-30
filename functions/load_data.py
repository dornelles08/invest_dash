from functions.get_fii_details import get_fii
from services.fiis import FiisService
from services.transaction import TransactionsService


def load_fiis(user_id):
    """
        Busca todas informações de Fiis
    """
    fiis_service = FiisService()
    fiis = fiis_service.get_fiis(user_id)

    fiis_category = {}
    for fii in fiis:
        fiis_category[fii["ativo"]] = fii["category"]

    fiis_names = []
    for fii in fiis:
        fiis_names.append(fii["ativo"])

    return fiis, fiis_category, fiis_names


def get_fiis_infos(st, user_id):
    """
        Busca os informações dos Fiis
    """
    BAR = st.progress(0, text="Buscando Informações Atualizadas")
    # _, _, fiis, _ = load_fiis(user_id)
    transaction_service = TransactionsService()
    fiis = transaction_service.get_fiis_from_transactions(user_id)
    fiis_details = []
    for i, fii in enumerate(fiis):
        percent = i/(len(fiis)-1)

        BAR.progress(percent, text=fii)
        data = get_fii(fii)
        fiis_details.append(data)

    return fiis_details

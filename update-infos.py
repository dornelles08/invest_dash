import time
from datetime import datetime

import schedule

from functions.get_fii_details import get_fii
from services.dados import DadosService
from services.transaction import TransactionsService
from services.user import UserService


def job():
    user_services = UserService()
    dados_service = DadosService()
    transaction_service = TransactionsService()

    users = user_services.get_users()

    for user in users:
        print(user["name"])

        fiis = transaction_service.get_fiis_from_transactions(user["_id"])
        fiis_details = []
        for _, fii in enumerate(fiis):
            data = get_fii(fii)
            fiis_details.append(data)

        dados_service.upsert_dados(fiis_details)
        user_services.update_user({
            **user,
            "sync": datetime.now().strftime("%x %X")
        })
        print("Dados Sincronizados")


print("Inicio")

schedule.every(15).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

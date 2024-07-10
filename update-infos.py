import time
from datetime import datetime

import schedule

from functions.get_fii_details import get_fii
from functions.load_data import load_fiis
from services.dados import DadosService
from services.user import UserService


def job():
    user_services = UserService()
    dados_service = DadosService()

    users = user_services.get_users()

    for user in users:
        print(user["name"])
        if (datetime.strptime(user["sync"], "%x %X") - datetime.now()).seconds > 900:
            print("Synced")
            continue

        _, _, fiis, _ = load_fiis(user["_id"])
        fiis_details = []
        for _, fii in enumerate(fiis):
            data = get_fii(fii)
            fiis_details.append(data)

        dados_service.upsert_dados(fiis_details)
        user_services.update_user({
            **user,
            "sync": datetime.now().strftime("%x %X")
        })


schedule.every(3).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

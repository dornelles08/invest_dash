import time

import schedule

from functions.get_fii_details import update_prices_month
from services.user import UserService


def job():
    user_service = UserService()

    users = user_service.get_users()

    for user in users:
        update_prices_month(user["_id"])


print("Inicio")

schedule.every().day.at("19:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1000)

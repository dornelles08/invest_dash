import time

import pandas as pd
import schedule

from functions.get_fii_details import get_fii
from functions.load_data import load_fiis


def job():
    _, _, fiis, _ = load_fiis()
    fiis_details = []
    for _, fii in enumerate(fiis):
        data = get_fii(fii)
        fiis_details.append(data)

    pd.DataFrame(data=fiis_details).to_csv("data/data.csv", index=False)

schedule.every(3).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

from datetime import datetime

import pandas as pd
import streamlit as st

from functions.configs import valid_user_logged
from services.dados import DadosService
from services.transaction import TransactionsService

date = datetime.now().strftime("%x %X")

date

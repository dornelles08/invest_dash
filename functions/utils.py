""" Arquivos com funções uteis utilizadas no sistema """
import calendar
from datetime import datetime


def convert_date(data_str):
    """ 
      Converter data do formato mes/ano para datetime 
    """
    return datetime.strptime(data_str, "%m/%Y")


def last_day_month(data_str):
    """ 
      Busca o último dia do mês referente
    """
    date = datetime.strptime(data_str, "%m/%Y")
    last_day = calendar.monthrange(date.year, date.month)[1]
    return datetime(date.year, date.month, last_day)

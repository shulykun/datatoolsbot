import sys
import os

sys.path.insert(0, '..')

import pandas as pd
from service.models import Term

def fill():
    """
        заполнение таблицы (Term) данными
        i в цикле это словарь с ключами - названиями полей в таблице
    """

    data = pd.read_excel('data/hw_terms_8.xlsx').to_dict(orient="rows")

    for i in data:
        
        s = Term(**i)
        s.save()


if __name__ == '__main__':
    fill()

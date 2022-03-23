import requests
import json
from config import keys


class convertException(Exception):
    pass


class ValuesConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise convertException(f'Нельзя перевести одинаковые валюты {base}')

        try:
            quote_tick = keys[quote]
        except KeyError:
            raise convertException(f'Ну удалось обработать валюту {quote}')

        try:
            base_tick = keys[base]
        except KeyError:
            raise convertException(f'Ну удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise convertException(f'Неверный формат количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_tick}&tsyms={base_tick}')
        resp = json.loads(r.content)
        total_base = resp[base_tick] * amount

        return total_base

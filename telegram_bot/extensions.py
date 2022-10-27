import requests
import json

import config


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        base = base.lower()
        quote = quote.lower()

        if base not in config.CURRENCIES or quote not in config.CURRENCIES:
            raise APIException("Нет такой валюты")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Введите количество валюты")

        if amount <= 0:
            raise APIException("Введите положительное число")

        payload = {'from': config.CURRENCIES.get(base),
                   'to': config.CURRENCIES.get(quote),
                   'amount': amount}
        api_url = f'https://api.exchangerate.host/convert'

        try:
            response = requests.get(api_url, params=payload)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise APIException("Ошибка! Ответ сервера: " + e.response.reason)
        except requests.exceptions.ConnectionError:
            raise APIException("Ошибка соединения с сервером!")
        except requests.RequestException as e:
            raise APIException(e)
        else:
            data = json.loads(response.text)

            print(data)
            result = data['result']
            if result is None:
                raise APIException("Сервер не смог выполнить преобразование")
            return round(result, 2)



if __name__ == "__main__":
    tests = [
        ("долларЫ", "рубль", 100),
        ("доллар", "рублИ", 100),
        ("доллар", "рубль", -1),
        ("доллар", "рубль", 0),
        ("доллар", "рубль", 100),
        ("Доллар", "руБль", 100),
    ]

    for t in tests:
        try:
            print(Convertor.get_price(*t))
        except APIException as e:
            print(e)
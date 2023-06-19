import requests
from time import sleep
import logging


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_response(url, params=None, await_time=10):
    while True:
        try:
            response = requests.get(url, params)
            break
        except requests.ConnectionError as err:
            logging.exception(err)
            logging.error('Проверьте интернет соединение, ожидание подключения.')
            sleep(await_time)
    return response
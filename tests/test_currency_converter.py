import os

import requests

from currency_converter.base import HeaderDict

API_HOST = os.getenv('API_HOST', 'http://localhost:9001')


def test_header_dict():
    headers = HeaderDict({ 'content-type': 'application/json' })
    assert 'CONTENT-TYPE' in headers
    assert headers['CoNtEnT-tYPe'] == 'application/json'


def test_echo():
    message = 'Hello'
    with requests.post(
            f'{API_HOST}/echo',
            json=dict(message=message),
        ) as r:
        assert r.json()['message'] == message[::-1]


def test_convert_rub_to_usd():
    with requests.get(f'{API_HOST}/convert/27/RUB/USD') as r:
        res = r.json()
        print(res)
        assert res['base'] == 'RUB'
        assert res['conversion']['USD'] < 1
        print('2007 не вернуть :-(')

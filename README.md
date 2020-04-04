```zsh
# Установка Poetry
$ yay -S python-poetry

# либо
$ pip install poetry

# Установка зависимостей
$ poetry install

# Запуск тестов
$ poetry run pytest -s tests

# Запуск
$ poetry run python -m currency_converter

# Без Poetry
$ PYTHONPATH=/path/to/currency-converter python -m currency_converter

# С помощью Docker

$ cd /path/to/src
$ docker build --tag currency-converter:0.1.0 .
$ docker run -p 9001:9001 -d --name conv currency-converter:0.1.0

$ http :9001/convert/100/USD/RUB
HTTP/1.1 200 OK
Content-Length: 114
Content-Type: application/json; charset=utf-8
Date: Sat, 04 Apr 2020 11:24:05 GMT
Server: BaseHTTP/0.6 Python/3.8.2

{
    "amount": 100.0,
    "conversion": {
        "RUB": 7678.02503477
    },
    "base": "USD",
    "date": "2020-04-03"
}

$ http :9001/convert/100/RUB/USD,EUR
HTTP/1.1 200 OK
Content-Length: 134
Content-Type: application/json; charset=utf-8
Date: Sat, 04 Apr 2020 11:24:21 GMT
Server: BaseHTTP/0.6 Python/3.8.2

{
    "amount": 100.0,
    "conversion": {
        "EUR": 1.20762008,
        "USD": 1.30241826
    },
    "base": "RUB",
    "date": "2020-04-03"
}

$ http post :9001/echo message=Hello
HTTP/1.1 200 OK
Content-Length: 24
Content-Type: application/json; charset=utf-8
Date: Sat, 04 Apr 2020 12:07:50 GMT
Server: BaseHTTP/0.6 Python/3.8.2

{
    "message": "olleH"
}
```

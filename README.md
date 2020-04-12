## Задание

[Сайт конторы](http://qmobi.agency). Ясное дело «лидеры», в партнерах перечислены название компаний, которые в голову взбрели копирайтеру. Отзывы на сайте скорее всего фейковые. Самое задание лежит в репозитории в формате pdf (смотрим). Вкратце: нужно было написать сервис без использования сторонних библиотек. Причем, чтобы пройти собеседование нужно было выполнить тестовое задание. Мне дадли на выполнение него три дня, я сделал за день, потратив кучу времени на наведение красоты. Само собеседование я завалил на вопросах о паттернах и алгоритмах. Эти вопросы я считаю неуместными, потому как коммерческая разработка предполагает использование готовых фреймворков, где все паттерны и алгоритмы за тебя реализованы, а эти ребята, как я понял, занимаются велосипедостроением. Это довольно частая ситуация когда говнокодер с манией величия учится за деньги работодателя, пилит свой pet-проект в виде очередного никому ненужного унылого говнофреймворка (нахуя он нужен без документации и коммъюнити?), чтобы в конечном итоге свалить в солнечную Калифорнию. Жалею, что потратил на этих мудаков свое драгоценное время.

## Инструкция

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

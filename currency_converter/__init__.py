import json
import logging
import os
import urllib.parse
import urllib.request

from .base import ApiServer, Endpoint
from .log import logger
from .version import __version__

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 9001))


class Greeting(Endpoint):
    path = '/'

    def get(self):
        return {'message': "Hello! 你好! Привет!"}


class Echo(Endpoint):
    path = '/echo'

    def post(self):
        return {'message': self.request.data['message'][::-1]}


class ConvertCurrency(Endpoint):
    path = '/convert/<amount>/<from>/<to>'

    def get(self):
        amount = float(self.request.parameters['amount'])
        base = self.request.parameters['from']
        symbols = self.request.parameters['to']

        qs = urllib.parse.urlencode(dict(base=base, symbols=symbols))
        url = 'https://api.exchangeratesapi.io/latest?' + qs
        with urllib.request.urlopen(url) as r:
            content = r.read().decode()
        result = json.loads(content)
        return {
            'base': result['base'],
            'amount': amount,
            'date': result['date'],
            'conversion': {
                k: v * amount
                for k, v in result['rates'].items()
            }
        }


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(name)-20s %(levelname)-10s %(asctime)-25s %(message)s')
    server = ApiServer(HOST, PORT)
    server.register_endpoint(Greeting)
    server.register_endpoint(Echo)
    server.register_endpoint(ConvertCurrency)
    try:
        ip, port = server.server_address
        logger.info(f'Server address: {ip}:{port}')
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        server.server_close()

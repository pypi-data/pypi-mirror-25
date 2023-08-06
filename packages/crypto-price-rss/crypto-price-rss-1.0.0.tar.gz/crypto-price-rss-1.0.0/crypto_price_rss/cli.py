#!/usr/bin/env python
import argparse
import os
import uuid
from datetime import datetime


from werkzeug.contrib.atom import AtomFeed
import requests


CRYPTO_URL = 'https://min-api.cryptocompare.com/data/price?fsym={from_symbol}&tsyms={to_symbol}'
CRYPTO_LIST = 'https://www.cryptocompare.com/api/data/coinlist/'
TARGET_CURRENCY = os.environ.get('TRADE_TARGET_CURRENCY', 'USD')
RESPONSE_TEMPLATE = '{symbol} is currently trading at {price} {target_currency}'


parser = argparse.ArgumentParser(description='Dump crypto RSS feed')
parser.add_argument('--file', help='Dump to specified file instead of stdout')
parser.add_argument('--symbols', default='btc', help='Symbols of currency, comma delimited')
args = parser.parse_args()


def main():
    response = requests.get(CRYPTO_LIST).json()
    crypto_data = {symbol.lower(): data for symbol, data in response['Data'].items()}

    feed = AtomFeed('Crypto Prices', feed_url='/', url='/', subtitle='Crypto updates for given symbols')
    for symbol in args.symbols.split(','):
        price, url = get_price(crypto_data, symbol)
        title = RESPONSE_TEMPLATE.format(symbol=symbol, price=price, target_currency=TARGET_CURRENCY)
        id = (str(uuid.uuid4()))
        author = 'crypto-price'
        date = datetime.utcnow()
        feed.add(title, "", content_type='html', author=author, url=url, id=id, published=date, updated=date)
    response = feed.get_response().response[0].decode("utf-8")
    if args.file:
        with open(args.file, 'w') as f:
            f.write(response)
    else:
        print(response)


def get_price(crypto_data, symbol='btc'):
    """ Test out of symbol is crypto, and if so return price. Throw ValueError otherwise. """
    if symbol not in crypto_data:
        for crypto_symbol, data in crypto_data.items():
            if data['CoinName'] == symbol:
                symbol = crypto_symbol
    if symbol in crypto_data:
        url = CRYPTO_URL.format(from_symbol=symbol.upper(), to_symbol=TARGET_CURRENCY)
        response = requests.get(url)
        price = response.json()[TARGET_CURRENCY]
        return float(price), url
    raise ValueError(symbol + ' not available as crypto')


if __name__ == "__main__":
    main()

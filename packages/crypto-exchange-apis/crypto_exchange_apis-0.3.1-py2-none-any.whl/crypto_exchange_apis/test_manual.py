# TuxExchange tests
from crypto_exchange_apis import Bittrex
from crypto_exchange_apis import Poloniex
from crypto_exchange_apis import Tuxexchange

bittrex = Bittrex()

print('Bittrex tests:')
print(str(bittrex.get_currencies())[0:77]+'...')
print(str(bittrex.get_markets())[0:77]+'...')

poloniex = Poloniex()

print('Poloniex tests:')
print(str(poloniex.returnTicker()['BTC_XMR'])[0:77]+'...')
print(str(poloniex.returnCurrencies())[0:77]+'...')

tuxexchange = Tuxexchange()

print('Tux Exchange tests:')
print(str(tuxexchange.api_query('getcoins'))[0:77]+'...')
print(str(tuxexchange.api_query('getticker'))[0:77]+'...')

Crypto Exchange APIs
====================

Inspired by BitEx_ written by nlsdfnbch_ (Python 3)

.. _BitEx: https://github.com/nlsdfnbch/bitex
.. _nlsdfnbch: https://github.com/nlsdfnbch

## Installation

Install with `pip` using `pip install crypto-exchange-apis`

Usage
-----

**Bittrex_ (`Bittrex API docs`)**

.. _Bittrex: https://bittrex.com
.. _`Bittrex API docs`: https://bittrex.com/home/api

test_manual.py_:::

  from crypto_exchange_apis import Bittrex

  bittrex = Bittrex()

  print bittrex.get_currencies()
  {'message': '', 'result': [{'Notice': None, 'TxFee': 0.001, 'CurrencyLo...
  print bittrex.get_markets()
  {'message': '', 'result': [{'Notice': None, 'Created': '2014-02-13T00:0...

**Poloniex_ (`Poloniex API docs`_)**

.. _Poloniex: https://poloniex.com
.. _`Poloniex API docs`: https://poloniex.com/support/api

test_manual.py_:::

  from crypto_exchange_apis import Poloniex

  poloniex = Poloniex()

  poloniex.returnTicker()['BTC_XMR']
  {'last': 0.01929211, 'quoteVolume': 29239.14327161, 'high24hr': 0.02068574...

**`Tux Exchange`_ (`Tux Exchange API docs`_)**

.. _`Tux Exchange`: https://tuxexchange.com
.. _`Tux Exchange API docs`: https://tuxexchange.com/docs

test_manual.py_:::

  from crypto_exchange_apis import Tuxexchange

  tuxexchange = Tuxexchange()

  print tuxexchange.api_query('getcoins')
  {'PPC': {'website': 'www.peercoin.org', 'minconfs': '2', 'name': 'Peer...
  print tuxexchange.api_query('getticker')
  {'BTC_ICN': {'last': '0.00040418', 'quoteVolume': '0', 'high24hr': '0'...

.. _test_manual.py: https://github.com/init-industries/crypto-exchange-apis/blob/master/crypto_exchange_apis/test_manual.py

Testing
-------

Run unit tests in test.py_

.. test.py: https://github.com/init-industries/crypto-exchange-apis/blob/master/crypto_exchange_apis/test.py

## Credits

Uses:

 - `python-bittrex`_ by ericsomdahl_()

.. _`python-bittrex`: https://github.com/ericsomdahl/python-bittrex
.. _ericsomdahl: https://github.com/ericsomdahl

 - poloniex_ by Aula13_

.. _poloniex: https://github.com/Aula13/poloniex
.. _Aula13: https://github.com/Aula13



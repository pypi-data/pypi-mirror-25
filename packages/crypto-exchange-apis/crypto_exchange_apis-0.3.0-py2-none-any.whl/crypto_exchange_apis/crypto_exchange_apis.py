'''
  Cryptocurrency exchange API wrappers tested on Python 2.7.12
  https://github.com/init-industries/crypto-exchange-

  See docs folder
'''

import time
import json
try:
  from urllib import urlencode
  from urlparse import urljoin
except ImportError:
  from urllib.parse import urlencode
  from urllib.parse import urljoin

import hmac
import hashlib
try:
  from Crypto.Cipher import AES
except ImportError:
  encrypted = False
else:
  import getpass
  import ast
  import json
  encrypted = True

import requests

# Poloniex-specific imports
import six as six
import itertools as itertools
import threading as threading
from concurrency import RecurrentTimer, Semaphore
from utils import AutoCastDict

BITTREX_BASE_URL = 'https://bittrex.com/api/v1.1/{method_set}/{method}?' # see https://bittrex.com/home/api
POLONIEX_PUBLIC_BASE_URL = 'https://poloniex.com/public' # see https://poloniex.com/support/api/
POLONIEX_ATHENTICATED_BASE_URL = 'https://poloniex.com/tradingApi'
TUXEXCHANGE_BASE_URL = 'https://tuxexchange.com/api?method={method}' # see https://tuxexchange.com/docs

# Possible methods
TUXEXCHANGE_PUBLIC_METHODS = [
  'getticker',
  'get24hvolume',
  'getorders',
  'gettradehistory',
  'getcoins']

BITTREX_AUTHENTICATED_MARKET_METHODS = {
  'getopenorders',
  'cancel',
  'sellmarket',
  'selllimit',
  'buymarket',
  'buylimit'
}
BITTREX_AUTHENTICATED_ACCOUNT_METHODS = {
  'getbalances',
  'getbalance',
  'getdepositaddress',
  'withdraw',
  'getorderhistory',
  'getorder',
  'getdeposithistory',
  'getwithdrawalhistory'
}
TUXEXCHANGE_AUTHENTICATED_METHODS = [
  'getmybalances',
  'withdraw',
  'getmyaddresses',
  'getmytradehistory',
  'buy',
  'sell',
  'getmyopenorders',
  'cancelorder']


def using_requests(request_url, apisign=None):
  if apisign:
    return  requests.get(
              request_url,
              headers={'apisign': apisign}
            ).json()
  else:
    return  requests.get(
              request_url
            ).json()


def encrypt(api_key, api_secret, export=True, export_fn='auth.json'):
  cipher = AES.new(getpass.getpass('Input encryption password (string will not show)'))
  api_key_n = cipher.encrypt(api_key)
  api_secret_n = cipher.encrypt(api_secret)
  api = {'key': str(api_key_n), 'secret': str(api_secret_n)}
  if export:
    with open(export_fn, 'w') as outfile:
      json.dump(api, outfile)
  return api


class Bittrex(object):
  '''
  Bittrex API wrapper
  '''
  def __init__(self, api_key=None, api_secret=None, calls_per_second=1, dispatch=using_requests):
    self.api_key = str(api_key) if api_key is not None else ''
    self.api_secret = str(api_secret) if api_secret is not None else ''
    self.dispatch = dispatch
    self.call_rate = 1.0/calls_per_second
    self.last_call = None

  def decrypt(self):
    if encrypted:
      cipher = AES.new(getpass.getpass(
        'Input decryption password (string will not show)'))
      try:
        if isinstance(self.api_key, str):
          self.api_key = ast.literal_eval(self.api_key)
        if isinstance(self.api_secret, str):
          self.api_secret = ast.literal_eval(self.api_secret)
      except Exception:
        pass
      self.api_key = cipher.decrypt(self.api_key).decode()
      self.api_secret = cipher.decrypt(self.api_secret).decode()
    else:
      raise ImportError('pycrypto module has to be installed')

  def wait(self):
    if self.last_call is None:
      self.last_call = time.time()
    else:
      now = time.time()
      passed = now - self.last_call
      if passed < self.call_rate:
        #print('sleep')
        time.sleep(1.0 - passed)

      self.last_call = time.time()

  def api_query(self, method, options=None):
    '''
    Queries Bittrex with given method and options.

    :param method: Query method for getting info
    :type method: str
    :param options: Extra options for query
    :type options: dict
    :return: JSON response from Bittrex
    :rtype : dict
    '''
    if not options:
      options = {}
    nonce = str(int(time.time() * 1000))
    method_set = 'public'

    if method in BITTREX_AUTHENTICATED_MARKET_METHODS:
      method_set = 'market'
    elif method in BITTREX_AUTHENTICATED_ACCOUNT_METHODS:
      method_set = 'account'

    request_url = BITTREX_BASE_URL.format(method_set=method_set, method=method)

    if method_set != 'public':
      request_url = '{0}apikey={1}&nonce={2}&'.format(
        request_url, self.api_key, nonce)

    request_url += urlencode(options)

    apisign = hmac.new(self.api_secret.encode(),
                       request_url.encode(),
                       hashlib.sha512).hexdigest()

    self.wait()

    return self.dispatch(request_url, apisign)

  def get_markets(self):
    '''
    Used to get the open and available trading markets
    at Bittrex along with other meta data.

    Endpoint: /public/getmarkets

    Example ::
      {'success': True,
       'message': '',
       'result': [ {'MarketCurrency': 'LTC',
              'BaseCurrency': 'BTC',
              'MarketCurrencyLong': 'Litecoin',
              'BaseCurrencyLong': 'Bitcoin',
              'MinTradeSize': 1e-08,
              'MarketName': 'BTC-LTC',
              'IsActive': True,
              'Created': '2014-02-13T00:00:00',
              'Notice': None,
              'IsSponsored': None,
              'LogoUrl': 'https://i.imgur.com/R29q3dD.png'},
              ...
            ]
      }

    :return: Available market info in JSON
    :rtype : dict
    '''
    return self.api_query('getmarkets')

  def get_currencies(self):
    '''
    Used to get all supported currencies at Bittrex
    along with other meta data.

    Endpoint: /public/getcurrencies

    :return: Supported currencies info in JSON
    :rtype : dict
    '''
    return self.api_query('getcurrencies')

  def get_ticker(self, market):
    '''
    Used to get the current tick values for a market.

    Endpoint: /public/getticker

    :param market: String literal for the market (ex: BTC-LTC)
    :type market: str
    :return: Current values for given market in JSON
    :rtype : dict
    '''
    return self.api_query('getticker', {'market': market})

  def get_market_summaries(self):
    '''
    Used to get the last 24 hour summary of all active exchanges

    Endpoint: /public/getmarketsummary

    :return: Summaries of active exchanges in JSON
    :rtype : dict
    '''
    return self.api_query('getmarketsummaries')

  def get_marketsummary(self, market):
    '''
    Used to get the last 24 hour summary of all active
    exchanges in specific coin

    Endpoint: /public/getmarketsummary

    :param market: String literal for the market(ex: BTC-XRP)
    :type market: str
    :return: Summaries of active exchanges of a coin in JSON
    :rtype : dict
    '''
    return self.api_query('getmarketsummary', {'market': market})

  def get_orderbook(self, market, depth_type, depth=20):
    '''
    Used to get retrieve the orderbook for a given market

    Endpoint: /public/getorderbook

    :param market: String literal for the market (ex: BTC-LTC)
    :type market: str
    :param depth_type: buy, sell or both to identify the type of
      orderbook to return.
      Use constants BUY_ORDERBOOK, SELL_ORDERBOOK, BOTH_ORDERBOOK
    :type depth_type: str
    :param depth: how deep of an order book to retrieve.
      Max is 100, default is 20
    :type depth: int
    :return: Orderbook of market in JSON
    :rtype : dict
    '''
    return self.api_query('getorderbook',
                          {'market': market,
                           'type': depth_type,
                           'depth': depth})

  def get_market_history(self, market, count=20):
    '''
    Used to retrieve the latest trades that have occurred for a
    specific market.

    Endpoint: /market/getmarkethistory

    Example ::
      {'success': True,
      'message': '',
      'result': [ {'Id': 5625015,
             'TimeStamp': '2017-08-31T01:29:50.427',
             'Quantity': 7.31008193,
             'Price': 0.00177639,
             'Total': 0.01298555,
             'FillType': 'FILL',
             'OrderType': 'BUY'},
             ...
             ]
      }

    :param market: String literal for the market (ex: BTC-LTC)
    :type market: str
    :param count: Number between 1-100 for the number
      of entries to return (default = 20)
    :type count: int
    :return: Market history in JSON
    :rtype : dict
    '''
    return self.api_query('getmarkethistory',
                          {'market': market, 'count': count})

  def buy_limit(self, market, quantity, rate):
    '''
    Used to place a buy order in a specific market. Use buylimit to place
    limit orders Make sure you have the proper permissions set on your
    API keys for this call to work

    Endpoint: /market/buylimit

    :param market: String literal for the market (ex: BTC-LTC)
    :type market: str
    :param quantity: The amount to purchase
    :type quantity: float
    :param rate: The rate at which to place the order.
      This is not needed for market orders
    :type rate: float
    :return:
    :rtype : dict
    '''
    return self.api_query('buylimit',
                          {'market': market,
                           'quantity': quantity,
                           'rate': rate})

  def sell_limit(self, market, quantity, rate):
    '''
    Used to place a sell order in a specific market. Use selllimit to place
    limit orders Make sure you have the proper permissions set on your
    API keys for this call to work

    Endpoint: /market/selllimit

    :param market: String literal for the market (ex: BTC-LTC)
    :type market: str
    :param quantity: The amount to purchase
    :type quantity: float
    :param rate: The rate at which to place the order.
      This is not needed for market orders
    :type rate: float
    :return:
    :rtype : dict
    '''
    return self.api_query('selllimit',
                          {'market': market,
                           'quantity': quantity,
                           'rate': rate})

  def cancel(self, uuid):
    '''
    Used to cancel a buy or sell order

    Endpoint: /market/cancel

    :param uuid: uuid of buy or sell order
    :type uuid: str
    :return:
    :rtype : dict
    '''
    return self.api_query('cancel', {'uuid': uuid})

  def get_open_orders(self, market=None):
    '''
    Get all orders that you currently have opened.
    A specific market can be requested.

    Endpoint: /market/getopenorders

    :param market: String literal for the market (ie. BTC-LTC)
    :type market: str
    :return: Open orders info in JSON
    :rtype : dict
    '''
    return self.api_query('getopenorders',
                          {'market': market} if market else None)

  def get_balances(self):
    '''
    Used to retrieve all balances from your account.

    Endpoint: /account/getbalances

    Example ::
      {'success': True,
       'message': '',
       'result': [ {'Currency': '1ST',
              'Balance': 10.0,
              'Available': 10.0,
              'Pending': 0.0,
              'CryptoAddress': None},
              ...
            ]
      }


    :return: Balances info in JSON
    :rtype : dict
    '''
    return self.api_query('getbalances', {})

  def get_balance(self, currency):
    '''
    Used to retrieve the balance from your account for a specific currency

    Endpoint: /account/getbalance

    Example ::
      {'success': True,
       'message': '',
       'result': {'Currency': '1ST',
            'Balance': 10.0,
            'Available': 10.0,
            'Pending': 0.0,
            'CryptoAddress': None}
      }


    :param currency: String literal for the currency (ex: LTC)
    :type currency: str
    :return: Balance info in JSON
    :rtype : dict
    '''
    return self.api_query('getbalance', {'currency': currency})

  def get_deposit_address(self, currency):
    '''
    Used to generate or retrieve an address for a specific currency

    Endpoint: /account/getdepositaddress

    :param currency: String literal for the currency (ie. BTC)
    :type currency: str
    :return: Address info in JSON
    :rtype : dict
    '''
    return self.api_query('getdepositaddress', {'currency': currency})

  def withdraw(self, currency, quantity, address):
    '''
    Used to withdraw funds from your account

    Endpoint: /account/withdraw

    :param currency: String literal for the currency (ie. BTC)
    :type currency: str
    :param quantity: The quantity of coins to withdraw
    :type quantity: float
    :param address: The address where to send the funds.
    :type address: str
    :return:
    :rtype : dict
    '''
    return self.api_query('withdraw',
                          {'currency': currency,
                           'quantity': quantity,
                           'address': address})

  def get_order_history(self, market=None):
    '''
    Used to retrieve order trade history of account

    Endpoint: /account/getorderhistory

    :param market: optional a string literal for the market (ie. BTC-LTC).
      If omitted, will return for all markets
    :type market: str
    :return: order history in JSON
    :rtype : dict
    '''
    return self.api_query('getorderhistory',
                          {'market': market} if market else None)

  def get_order(self, uuid):
    '''
    Used to get details of buy or sell order

    Endpoint: /account/getorder

    :param uuid: uuid of buy or sell order
    :type uuid: str
    :return:
    :rtype : dict
    '''
    return self.api_query('getorder', {'uuid': uuid})

  def get_withdrawal_history(self, currency=None):
    '''
    Used to view your history of withdrawals

    Endpoint: /account/getwithdrawalhistory

    :param currency: String literal for the currency (ie. BTC)
    :type currency: str
    :return: withdrawal history in JSON
    :rtype : dict
    '''

    return self.api_query('getwithdrawalhistory',
                          {'currency': currency} if currency else None)

  def get_deposit_history(self, currency=None):
    '''
    Used to view your history of deposits

    Endpoint: /account/getdeposithistory

    :param currency: String literal for the currency (ie. BTC)
    :type currency: str
    :return: deposit history in JSON
    :rtype : dict
    '''
    return self.api_query('getdeposithistory',
                          {'currency': currency} if currency else None)

  def list_markets_by_currency(self, currency):
    '''
    Helper function to see which markets exist for a currency.

    Endpoint: /public/getmarkets

    Example ::
      >>> Bittrex(None, None).list_markets_by_currency('LTC')
      ['BTC-LTC', 'ETH-LTC', 'USDT-LTC']

    :param currency: String literal for the currency (ex: LTC)
    :type currency: str
    :return: List of markets that the currency appears in
    :rtype: list
    '''
    return [market['MarketName'] for market in self.get_markets()['result']
      if market['MarketName'].lower().endswith(currency.lower())]


def _api_wrapper(fn):
  '''
  API function decorator that performs rate limiting and error checking.
  '''

  def _convert(value):
    if isinstance(value, datetime.date):
      return value.strftime('%s')
    return value

  @six.wraps(fn)
  def _fn(self, command, **params):
    # sanitize the params by removing the None values
    with self.startup_lock:
      if self.timer.ident is None:
        self.timer.setDaemon(True)
        self.timer.start()
    params = dict((key, _convert(value))
                  for key, value in six.iteritems(params)
                  if value is not None)

    self.semaphore.acquire()
    resp = fn(self, command, **params).json(object_hook=AutoCastDict)
    if 'error' in resp:
      raise Exception(resp['error'])
    return resp

  return _fn


class PoloniexPublic(object):
  '''
  Poloniex public API wrapper
  '''

  def __init__(self, public_url=POLONIEX_PUBLIC_BASE_URL, limit=6,
               session_class=requests.Session,
               session=None, startup_lock=None,
               semaphore=None, timer=None):
    '''
    Initialize Poloniex client.
    '''
    self._public_url = public_url
    self.startup_lock = startup_lock or threading.RLock()
    self.semaphore = semaphore or Semaphore(limit)
    self.timer = timer or RecurrentTimer(1.0, self.semaphore.clear)
    self.session = session or session_class()

  def __del__(self):
    self.timer.cancel()
    if self.timer.ident is not None:  # timer was started
      self.timer.join()

  @_api_wrapper
  def _public(self, command, **params):
    '''
    Invoke the 'command' public API with optional params.
    '''
    params['command'] = command
    return self.session.get(self._public_url, params=params)

  def returnTicker(self):
    '''
    Returns the ticker for all markets.
    '''
    return self._public('returnTicker')

  def return24hVolume(self):
    '''
    Returns the 24-hour volume for all markets, plus totals for
    primary currencies.
    '''
    return self._public('return24hVolume')

  def returnOrderBook(self, currencyPair='all', depth='50'):
    '''
    Returns the order book for a given market, as well as a sequence
    number for use with the Push API and an indicator specifying whether
    the market is frozen. You may set currencyPair to 'all' to get the
    order books of all markets.
    '''
    return self._public('returnOrderBook', currencyPair=currencyPair,
                        depth=depth)

  def returnTradeHistory(self, currencyPair, start=None, end=None):
    '''
    Returns the past 200 trades for a given market, or up to 50,000
    trades between a range specified in UNIX timestamps by the 'start'
    and 'end' GET parameters.
    '''
    return self._public('returnTradeHistory', currencyPair=currencyPair,
                        start=start, end=end)

  def returnChartData(self, currencyPair, period, start=0, end=2**32-1):
    '''
    Returns candlestick chart data. Required GET parameters are
    'currencyPair', 'period' (candlestick period in seconds; valid values
    are 300, 900, 1800, 7200, 14400, and 86400), 'start', and 'end'.
    'Start' and 'end' are given in UNIX timestamp format and used to
    specify the date range for the data returned.
    '''
    return self._public('returnChartData', currencyPair=currencyPair,
                        period=period, start=start, end=end)

  def returnCurrencies(self):
    '''
    Returns information about currencies.
    '''
    return self._public('returnCurrencies')

  def returnLoanOrders(self, currency):
    '''
    Returns the list of loan offers and demands for a given currency,
    specified by the 'currency' GET parameter.
    '''
    return self._public('returnLoanOrders', currency=currency)


class Poloniex(PoloniexPublic):
  '''
  Poloniex authenticated API wrapper.
  '''

  class _PoloniexAuth(requests.auth.AuthBase):

    '''
    Poloniex Request Authentication.
    '''

    def __init__(self, apikey, secret):
      self._apikey, self._secret = apikey, secret

    def __call__(self, request):
      signature = hmac.new(self._secret, request.body, hashlib.sha512)
      request.headers.update({'Key': self._apikey,
                              'Sign': signature.hexdigest()})
      return request

  def __init__(self, apikey=None, secret=None,
               public_url=POLONIEX_PUBLIC_BASE_URL,
               private_url=POLONIEX_ATHENTICATED_BASE_URL,
               limit=6, session_class=requests.Session,
               session=None, startup_lock=None,
               semaphore=None, timer=None,
               nonce_iter=None, nonce_lock=None):
    '''
    Initialize the Poloniex private client.
    '''
    super(Poloniex, self).__init__(public_url, limit,
                                   session_class,
                                   session, startup_lock,
                                   semaphore, timer)
    self._private_url = private_url
    self._apikey = apikey
    self._secret = secret
    self.nonce_lock = nonce_lock or threading.RLock()
    self.nonce_iter = nonce_iter or itertools.count(int(time.time() * 1000))

  @_api_wrapper
  def _private(self, command, **params):
    '''
    Invoke the 'command' public API with optional params.
    '''
    if not self._apikey or not self._secret:
      raise Exception('missing apikey/secret')

    with self.nonce_lock:
      params.update({'command': command, 'nonce': next(self.nonce_iter)})
      return self.session.post(
        self._private_url, data=params,
        auth=Poloniex._PoloniexAuth(self._apikey, self._secret))

  def returnBalances(self):
    '''
    Returns all of your available balances.
    '''
    return self._private('returnBalances')

  def returnCompleteBalances(self, account=None):
    '''
    Returns all of your balances, including available balance, balance
    on orders, and the estimated BTC value of your balance. By default,
    this call is limited to your exchange account; set the 'account' POST
    parameter to 'all' to include your margin and lending accounts.
    '''
    return self._private('returnCompleteBalances', account=account)

  def returnDepositAddresses(self):
    '''
    Returns all of your deposit addresses.
    '''
    return self._private('returnDepositAddresses')

  def generateNewAddress(self, currency):
    '''
    Generates a new deposit address for the currency specified by the
    'currency' POST parameter. Only one address per currency per day may be
    generated, and a new address may not be generated before the
    previously-generated one has been used.
    '''
    return self._private('generateNewAddress', currency=currency)

  def returnDepositsWithdrawals(self, start=0, end=2**32-1):
    '''
    Returns your deposit and withdrawal history within a range,
    specified by the 'start' and 'end' POST parameters, both of which
    should be given as UNIX timestamps.
    '''
    return self._private('returnDepositsWithdrawals', start=start, end=end)

  def returnDeposits(self, start=0, end=2**32-1):
    '''
    Returns your deposit history within a range, specified by the
    'start' and 'end' POST parameters, both of which should be given as
    UNIX timestamps.
    '''
    return self.returnDepositsWithdrawals(start, end)['deposits']

  def returnWithdrawals(self, start=0, end=2**32-1):
    '''
    Returns your withdrawal history within a range, specified by the
    'start' and 'end' POST parameters, both of which should be given as
    UNIX timestamps.
    '''
    return self.returnDepositsWithdrawals(start, end)['withdrawals']

  def returnOpenOrders(self, currencyPair='all'):
    '''
    Returns your open orders for a given market, specified by the
    'currencyPair' POST parameter, e.g. 'BTC_XCP'. Set 'currencyPair' to
    'all' to return open orders for all markets.
    '''
    return self._private('returnOpenOrders', currencyPair=currencyPair)

  def returnTradeHistory(self, currencyPair='all', start=None, end=None):
    '''
    Returns your trade history for a given market, specified by the
    'currencyPair' POST parameter. You may specify 'all' as the
    currencyPair to receive your trade history for all markets. You may
    optionally specify a range via 'start' and/or 'end' POST parameters,
    given in UNIX timestamp format; if you do not specify a range, it will
    be limited to one day.
    '''
    return self._private('returnTradeHistory', currencyPair=currencyPair,
                         start=start, end=end)

  def returnTradeHistoryPublic(self, currencyPair, start=None, end=None):
    '''
    Returns the past 200 trades for a given market, or up to 50,000
    trades between a range specified in UNIX timestamps by the 'start'
    and 'end' GET parameters.
    '''
    return super(Poloniex, self).returnTradeHistory(currencyPair, start, end)

  def returnOrderTrades(self, orderNumber):
    '''
    Returns all trades involving a given order, specified by the
    'orderNumber' POST parameter. If no trades for the order have occurred
    or you specify an order that does not belong to you, you will receive
    an error.
    '''
    return self._private('returnOrderTrades', orderNumber=orderNumber)

  def buy(self, currencyPair, rate, amount, fillOrKill=None,
          immediateOrCancel=None, postOnly=None):
    '''
    Places a limit buy order in a given market. Required POST parameters
    are 'currencyPair', 'rate', and 'amount'. If successful, the method
    will return the order number.
    You may optionally set 'fillOrKill', 'immediateOrCancel', 'postOnly'
    to 1. A fill-or-kill order will either fill in its entirety or be
    completely aborted. An immediate-or-cancel order can be partially or
    completely filled, but any portion of the order that cannot be filled
    immediately will be canceled rather than left on the order book.
    A post-only order will only be placed if no portion of it fills
    immediately; this guarantees you will never pay the taker fee on any
    part of the order that fills.
    '''
    return self._private('buy', currencyPair=currencyPair, rate=rate,
                         amount=amount, fillOrKill=fillOrKill,
                         immediateOrCancel=immediateOrCancel,
                         postOnly=postOnly)

  def sell(self, currencyPair, rate, amount, fillOrKill=None,
           immediateOrCancel=None, postOnly=None):
    '''
    Places a sell order in a given market. Parameters and output are
    the same as for the buy method.
    '''
    return self._private('sell', currencyPair=currencyPair, rate=rate,
                         amount=amount, fillOrKill=fillOrKill,
                         immediateOrCancel=immediateOrCancel,
                         postOnly=postOnly)

  def cancelOrder(self, orderNumber):
    '''
    Cancels an order you have placed in a given market. Required POST
    parameter is 'orderNumber'.
    '''
    return self._private('cancelOrder', orderNumber=orderNumber)

  def moveOrder(self, orderNumber, rate, amount=None, postOnly=None,
                immediateOrCancel=None):
    '''
    Cancels an order and places a new one of the same type in a single
    atomic transaction, meaning either both operations will succeed or both
     will fail. Required POST parameters are 'orderNumber' and 'rate'; you
     may optionally specify 'amount' if you wish to change the amount of
     the new order. 'postOnly' or 'immediateOrCancel' may be specified for
     exchange orders, but will have no effect on margin orders.
     '''
    return self._private('moveOrder', orderNumber=orderNumber, rate=rate,
                         amount=amount, postOnly=postOnly,
                         immediateOrCancel=immediateOrCancel)

  def withdraw(self, currency, amount, address, paymentId=None):
    '''
    Immediately places a withdrawal for a given currency, with no email
    confirmation. In order to use this method, the withdrawal privilege
    must be enabled for your API key. Required POST parameters are
    'currency', 'amount', and 'address'. For XMR withdrawals, you may
    optionally specify 'paymentId'.
    '''
    return self._private('withdraw', currency=currency, amount=amount,
                         address=address, paymentId=paymentId)

  def returnFeeInfo(self):
    '''
    If you are enrolled in the maker-taker fee schedule, returns your
    current trading fees and trailing 30-day volume in BTC. This
    information is updated once every 24 hours.
    '''
    return self._private('returnFeeInfo')

  def returnAvailableAccountBalances(self, account=None):
    '''
    Returns your balances sorted by account. You may optionally specify
    the 'account' POST parameter if you wish to fetch only the balances of
    one account. Please note that balances in your margin account may not
    be accessible if you have any open margin positions or orders.
    '''
    return self._private('returnAvailableAccountBalances', account=account)

  def returnTradableBalances(self):
    '''
    Returns your current tradable balances for each currency in each
    market for which margin trading is enabled. Please note that these
    balances may vary continually with market conditions.
    '''
    return self._private('returnTradableBalances')

  def transferBalance(self, currency, amount, fromAccount, toAccount):
    '''
    Transfers funds from one account to another (e.g. from your exchange
     account to your margin account). Required POST parameters are
     'currency', 'amount', 'fromAccount', and 'toAccount'.
     '''
    return self._private('transferBalance', currency=currency,
                           amount=amount, fromAccount=fromAccount,
                           toAccount=toAccount)

  def returnMarginAccountSummary(self):
    '''
    Returns a summary of your entire margin account. This is the same
    information you will find in the Margin Account section of the Margin
    Trading page, under the Markets list.
    '''
    return self._private('returnMarginAccountSummary')

  def marginBuy(self, currencyPair, rate, amount, lendingRate=None):
    '''
    Places a margin buy order in a given market. Required POST
    parameters are 'currencyPair', 'rate', and 'amount'. You may optionally
     specify a maximum lending rate using the 'lendingRate' parameter.
     If successful, the method will return the order number and any trades
     immediately resulting from your order.
     '''
    return self._private('marginBuy', currencyPair=currencyPair, rate=rate,
                           amount=amount, lendingRate=lendingRate)

  def marginSell(self):
    '''
    Places a margin sell order in a given market. Parameters and output
    are the same as for the marginBuy method.
    '''
    return self._private('marginSell')

  def getMarginPosition(self, currencyPair):
    '''
    Returns information about your margin position in a given market,
    specified by the 'currencyPair' POST parameter. You may set
    'currencyPair' to 'all' if you wish to fetch all of your margin
    positions at once. If you have no margin position in the specified
    market, 'type' will be set to 'none'. 'liquidationPrice' is an
    estimate, and does not necessarily represent the price at which an
    actual forced liquidation will occur. If you have no liquidation
    price, the value will be -1.
    '''
    return self._private('getMarginPosition', currencyPair=currencyPair)

  def closeMarginPosition(self, currencyPair):
    '''
    Closes your margin position in a given market (specified by the
    'currencyPair' POST parameter) using a market order. This call will
    also return success if you do not have an open position in the
    specified market.
    '''
    return self._private('closeMarginPosition', currencyPair=currencyPair)

  def createLoanOffer(self, currency, amount, duration, autoRenew,
                      lendingRate):
    '''
    Creates a loan offer for a given currency. Required POST parameters
    are 'currency', 'amount', 'duration', 'autoRenew' (0 or 1), and
    'lendingRate'.
    '''
    return self._private('createLoanOffer', currency=currency,
                         amount=amount, duration=duration,
                         autoRenew=autoRenew, lendingRate=lendingRate)

  def cancelLoanOffer(self, orderNumber):
    '''
    Cancels a loan offer specified by the 'orderNumber' POST
    parameter.
    '''
    return self._private('cancelLoanOffer', orderNumber=orderNumber)

  def returnOpenLoanOffers(self):
    '''
    Returns your open loan offers for each currency.
    '''
    return self._private('returnOpenLoanOffers')

  def returnActiveLoans(self):
    '''
    Returns your active loans for each currency.
    '''
    return self._private('returnActiveLoans')

  def returnLendingHistory(self, start=0, end=2**32-1, limit=None):
    '''
    Returns your lending history within a time range specified by the
    'start' and 'end' POST parameters as UNIX timestamps. 'limit' may also
    be specified to limit the number of rows returned.
    '''
    return self._private('returnLendingHistory', start=start, end=end,
                         limit=limit)

  def toggleAutoRenew(self, orderNumber):
    '''
    Toggles the autoRenew setting on an active loan, specified by the
    'orderNumber' POST parameter. If successful, 'message' will indicate
    the new autoRenew setting.
    '''
    return self._private('toggleAutoRenew', orderNumber=orderNumber)



class Tuxexchange(object):
  '''
  Tux Exchange API wrapper
  '''
  def __init__(self, calls_per_second=6, dispatch=using_requests):
    self.dispatch = dispatch
    self.call_rate = 1.0/calls_per_second
    self.last_call = None

  def wait(self):
    if self.last_call is None:
      self.last_call = time.time()
    else:
      now = time.time()
      passed = now - self.last_call
      if passed < self.call_rate:
        #print('sleep')
        time.sleep(1.0 - passed)

      self.last_call = time.time()

  def api_query(self, method, options=None):
    '''
    Queries Tux Exchange with given method and options.

    :param method: Method to query
    :return      : JSON response from Tux Exchange
    :rtype       : dict
    '''
    if not options:
      options = {}
    nonce = str(int(time.time() * 1000))

    request_url = TUXEXCHANGE_BASE_URL.format(method=method)

    request_url += urlencode(options)

    self.wait()

    return self.dispatch(request_url)

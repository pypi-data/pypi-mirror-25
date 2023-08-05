'''Bittrex API wrapper

See: https://bittrex.com/home/api

Notes
-----
Specify markets as 'btc-ltc' or 'BTC-LTC'
'''
import requests
import time
import hashlib
import hmac
import urllib
import json
import os
from urllib.parse import urlencode  # dict to 1=2&3=4
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


BASE_URL = 'https://bittrex.com/api/v1.1/{api_type}/{command}/?{kwargs}'
PUBLIC_SET = {
    'getmarkets',
    'getcurrencies',
    'getticker',
    'getmarketsummaries',
    'getmarketsummary',
    'getorderbook',
    'getmarkethistory'}
MARKET_SET = {
    'getopenorders',
    'cancel',
    'sellmarket',
    'selllimit',
    'buymarket',
    'buylimit'}
ACCOUNT_SET = {
    'getbalances',
    'getbalance',
    'getdepositaddress',
    'withdraw',
    'getorderhistory',
    'getorder',
    'getdeposithistory',
    'getwithdrawalhistory'}


class BittrexApiError(Exception):
    pass


class Bittrex():
    def __init__(self, *args, **kwargs):
        """Create Bittrex instance

        Checks args and kwargs for key/secret or file
        If it is supplied they get added, else they are ''
        API-documentation at: https://bittrex.com/home/api"""
        self.key = ''
        self.secret = ''
        if 'key' in kwargs and 'secret' in kwargs:
            self.key = kwargs['key']
            self.secret = kwargs['secret']
            logger.info('Add key and secret from kwargs')
        if len(args) == 1 and os.path.isfile(args[0]):
            self.load_key(args[0])
            logger.info('Load keys from args')
        if len(args) == 2:
            self.key = args[0]
            self.secret = args[1]
            logger.info('Add key and secret from args')

        self.public_calls = PUBLIC_SET
        self.market_calls = MARKET_SET
        self.account_calls = ACCOUNT_SET

    def add_key(self, key, secret):
        """Add key via arguments"""
        self.key = key
        self.secret = secret

    def load_key(self, filepath):
        """Load key from file"""
        with open(filepath, 'r') as f:
            lines = f.readlines()
            self.key, self.secret = [l.strip() for l in lines[:2]]

    def api_query(self, command, **kwargs):
        """Query the Bittrex API

        Parameters
        ----------
        command : string
            Required argument for the API query
        kwargs : dict
            Other parameters, required or optional, as described in
            https://bittrex.com/home/api

        Returns
        -------
        dict
            Request result is a JSON, will be parsed to a dict

        Raises
        ------
        BittrexApiError
            It the command is unknown
            If the request is not `ok`
            If the API does not return `success`
        """
        # Remove empty values from kwargs
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        # First check which API to use
        if command in PUBLIC_SET:
            api_type = 'public'
        elif command in MARKET_SET:
            api_type = 'market'
        elif command in ACCOUNT_SET:
            api_type = 'account'
        else:
            raise BittrexApiError(f'Command `{command}` not found')

        # Perform the actual request
        kwargs['apikey'] = self.key
        kwargs['nonce'] = int(time.time() * 1000)
        url = BASE_URL.format(
            command=command,
            api_type=api_type,
            kwargs=urlencode(kwargs))
        apisign = hmac.new(self.secret.encode(),
                           url.encode(),
                           hashlib.sha512).hexdigest()
        r = requests.get(url, headers={"apisign": apisign})

        # Minor error handling, then return
        if not r.ok:
            raise BittrexApiError('Request not okay')
        data = r.json()
        if not data['success']:
            raise BittrexApiError(f'Message: {data["message"]}, URL: {url}')
        return data['result']

    ###########################################################################
    # Public API
    def get_markets(self):
        """Get all open and available markets along with other meta data.

        Returns
        -------
        dict
            Available market info in JSON

        Notes
        -----
        Endpoint: /public/getmarkets
        Full Documentation: https://bittrex.com/home/api

        Example
        -------
        [{'MarketCurrency': 'LTC',
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
        """
        return self.api_query('getmarkets')

    def get_currencies(self):
        """Get all supported currencies at Bittrex along with other meta data.

        Returns
        -------
        dict
            Supported currencies info in JSON

        Notes
        -----
        Endpoint: /public/getcurrencies
        Full Documentation: https://bittrex.com/home/api
        """
        return self.api_query('getcurrencies')

    def get_ticker(self, market):
        """Get the current tick values for a market.

        Parameters
        ----------
        market : str
            String literal for the market (ex: BTC-LTC)

        Returns
        -------
        dict
            Current values for given market in JSON

        Notes
        -----
        Endpoint: /public/getticker
        Full Documentation: https://bittrex.com/home/api
        """
        return self.api_query('getticker', market=market)

    def get_market_summaries(self):
        """Get the last 24 hour summary of all active exchanges

        Returns
        -------
        dict
            Summaries of all active exchanges in JSON

        Notes
        -----
        Endpoint: /public/getmarketsummary
        Full Documentation: https://bittrex.com/home/api
        """
        return self.api_query('getmarketsummaries')

    def get_marketsummary(self, market):
        """Get the last 24 hour summary of specific market

        Parameters
        ----------
        market : str
            String literal for the market(ex: BTC-XRP)

        Returns
        -------
        dict
            Summary of requested market in JSON

        Notes
        -----
        Endpoint: /public/getmarketsummary
        Full Documentation: https://bittrex.com/home/api
        """
        return self.api_query('getmarketsummary', market=market)

    def get_orderbook(self, market, depth_type, depth=20):
        """Retrieve the orderbook for a given market

        Parameters
        ----------
        market : str
            String literal for the market (ex: BTC-LTC)
        depth_type : {'buy', 'sell', 'both'}
            Type of orderbook to return.
        depth : int
            How deep of an order book to retrieve.
            Max is 100, default is 20

        Returns
        -------
        dict
            Orderbook of market in JSON

        Notes
        -----
        Endpoint: /public/getorderbook
        Full Documentation: https://bittrex.com/home/api
        """
        return self.api_query(
            'getorderbook',
            market=market,
            type=depth_type,
            depth=depth)

    def get_market_history(self, market, count=20):
        """Retrieve the latest trades that have occurred for a
        specific market.

        Parameters
        ----------
        market : str
            String literal for the market (ex: BTC-LTC)
        count : int
            Number between 1-100 for the number of
            entries to return (default = 20)

        Returns
        -------
        dict
            Market history in JSON

        Notes
        -----
        Endpoint: /market/getmarkethistory
Full Documentation: https://bittrex.com/home/api

        Example
        -------
        [{'Id': 5625015,
          'TimeStamp': '2017-08-31T01:29:50.427',
          'Quantity': 7.31008193,
          'Price': 0.00177639,
          'Total': 0.01298555,
          'FillType': 'FILL',
          'OrderType': 'BUY'},
          ...
        ]
        """
        return self.api_query(
            'getmarkethistory',
            market=market,
            count=count)

    ###########################################################################
    # Market API
    def buy_limit(self, market, quantity, rate):
        """Place a buy order in a specific market.

        Use buylimit to placelimit orders. Make sure you have
        the proper permissions set on your API keys for this call to work

        Parameters
        ----------
        market : str
            String literal for the market (ex: BTC-LTC)
        quantity : float
            The amount to purchase
        rate : float
            The rate at which to place the order.
            This is not needed for market orders

        Returns
        -------
        dict
            Contains UUID of order

        Notes
        -----
        Endpoint: /market/buylimit
        Full Documentation: https://bittrex.com/home/api
        """
        return self.api_query(
            'buylimit',
            market=market,
            quantity=quantity,
            rate=rate)

    def sell_limit(self, market, quantity, rate):
        """Place a sell order in a specific market.

        Use selllimit to place limit orders. Make sure you have
        the proper permissions set on your API keys for this call to work

        Parameters
        ----------
        market : str
            String literal for the market (ex: BTC-LTC)
        quantity : float
            The amount to purchase
        rate : float
            The rate at which to place the order.
            This is not needed for market orders

        Returns
        -------
        dict
            Contains UUID of order

        Notes
        -----
        Endpoint: /market/selllimit
        Full Documentation: https://bittrex.com/home/api
        """
        return self.api_query(
            'selllimit',
            market=market,
            quantity=quantity,
            rate=rate)

    def cancel(self, uuid):
        """Cancel a buy or sell order

        Parameters
        ----------
        uuid : str
            uuid of buy or sell order

        Returns
        -------
        None
            Nothing to return if it worked, else api_query should
            raise a BittrexApiError

        Notes
        -----
        Endpoint: /market/cancel
        Full Documentation: https://bittrex.com/home/api
        """
        return self.api_query('cancel', uuid=uuid)

    def get_open_orders(self, market=None):
        """Get all orders that you currently have opened.

        A specific market can be requested.

        Parameters
        ----------
        market : str
            String literal for the market (ie. BTC-LTC)

        Returns
        -------
        dict
            Open orders info in JSON

        Notes
        -----
        Endpoint: /market/getopenorders
        Full Documentation: https://bittrex.com/home/api
        """
        return self.api_query(
            'getopenorders',
            market=market)

    ###########################################################################
    # Account API
    def get_balances(self):
        """Retrieve all balances from your account.

        Returns
        -------
        dict
            Balances info in JSON

        Notes
        -----
        Endpoint: /account/getbalances
Full Documentation: https://bittrex.com/home/api

        Example
        -------
        [{'Currency': '1ST',
          'Balance': 10.0,
          'Available': 10.0,
          'Pending': 0.0,
          'CryptoAddress': None},
          ...
        ]
        """
        return self.api_query('getbalances')

    def get_balance(self, currency):
        """Retrieve the balance from your account for a specific currency

        Parameters
        ----------
        currency : str
            String literal for the currency (ex: LTC)

        Returns
        -------
        dict
            Balance info in JSON

        Notes
        -----
        Endpoint: /account/getbalance
Full Documentation: https://bittrex.com/home/api

        Example
        -------
        {'Currency': '1ST',
         'Balance': 10.0,
         'Available': 10.0,
         'Pending': 0.0,
         'CryptoAddress': None}
        """
        return self.api_query('getbalance', currency=currency)

    def get_deposit_address(self, currency):
        """Generate or retrieve an address for a specific currency

        Parameters
        ----------
        currency : str
            String literal for the currency (ie. BTC)

        Returns
        -------
        dict
            Address info in JSON

        Notes
        -----
        Endpoint: /account/getdepositaddress
        Full Documentation: https://bittrex.com/home/api
        """
        return self.api_query('getdepositaddress', currency=currency)

    def withdraw(self, currency, quantity, address):
        """Withdraw funds from your account

        Parameters
        ----------
        currency : str
             String literal for the currency (ie. BTC)
        quantity : float
            The quantity of coins to withdraw
        address : str
            The address where to send the funds.

        Returns
        -------
        dict
            UUID of withdrawal

        Notes
        -----
        Endpoint: /account/withdraw
        Full Documentation: https://bittrex.com/home/api
        """
        return self.api_query(
            'withdraw',
            currency=currency,
            quantity=quantity,
            address=address)

    def get_order_history(self, market=None):
        """Retrieve order trade history of account

        Parameters
        ----------
        market : str
            optional a string literal for the market (ie. BTC-LTC).
            If omitted, will return for all markets

        Returns
        -------
        dict
            order history in JSON

        Notes
        -----
        Endpoint: /account/getorderhistory
        Full Documentation: https://bittrex.com/home/api
        """
        return self.api_query(
            'getorderhistory',
            market=market)

    def get_order(self, uuid):
        """Get details of buy or sell order

        Parameters
        ----------
        uuid : str
            uuid of buy or sell order

        Returns
        -------
        dict
            order

        Notes
        -----
        Endpoint: /account/getorder
        Full Documentation: https://bittrex.com/home/api
        """
        return self.api_query('getorder', uuid=uuid)

    def get_withdrawal_history(self, currency=None):
        """View your history of withdrawals

        Parameters
        ----------
        currency : str
            String literal for the currency (ie. BTC)

        Returns
        -------
        dict
            withdrawal history in JSON

        Notes
        -----
        Endpoint: /account/getwithdrawalhistory
        Full Documentation: https://bittrex.com/home/api
        """

        return self.api_query('getwithdrawalhistory',
                              currency=currency)

    def get_deposit_history(self, currency=None):
        """View your history of deposits

        Parameters
        ----------
        currency : str
            String literal for the currency (ie. BTC)

        Returns
        -------
        dict
            deposit history in JSON

        Notes
        -----
        Endpoint: /account/getdeposithistory
        Full Documentation: https://bittrex.com/home/api
        """
        return self.api_query('getdeposithistory',
                              currency=currency)


def examples():
    trex = Bittrex('sensitive/bittrex.key')
    trex.api_query('getmarkets')
    trex.api_query('getticker', market='btc-ltc')
    trex.api_query('getopenorders')


def main():
    pass


if __name__ == '__main__':
    main()

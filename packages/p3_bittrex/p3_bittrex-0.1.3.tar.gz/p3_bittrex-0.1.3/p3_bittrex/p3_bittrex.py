import os
import requests
import time
from urllib.parse import urlencode
import hmac
import hashlib
import json
from itertools import count

__version__ = "v1.1"

BASE_URL = "https://bittrex.com/api/" + __version__ + "/{service}/{method}?"
NONCE_COUNTER = count(int(time.time() * 1000))


MARKET_SET = {
    'getopenorders',
    'cancel',
    'sellmarket',
    'selllimit',
    'buymarket',
    'buylimit'
}

ACCOUNT_SET = {
    'getbalances',
    'getbalance',
    'getdepositaddress',
    'withdraw',
    'getorderhistory',
    'getorder',
    'getdeposithistory',
    'getwithdrawalhistory'
}


class Bittrex:

    def __init__(self, key=None, secret=None):

        if not key:
            key = os.environ['BITTREX_KEY']

        if not secret:
            secret = os.environ['BITTREX_SECRET']

        self.key = key
        self.secret = secret

    def query_engine(self, method, options=None):
        """
            engine of pi-bittrex
        """
        service = 'public'
        if method in MARKET_SET:
            service = 'market'
        elif method in ACCOUNT_SET:
            service = 'account'

        url = BASE_URL.format(service=service, method=method)

        if service != 'public':
            url += 'apikey={}&nonce={}&'.format(self.key, next(NONCE_COUNTER))

        if not options:
            options = {}

        url += urlencode(options)

        apisign = hmac.new(self.secret.encode(),
                           url.encode(),
                           hashlib.sha512).hexdigest()

        headers = {
            "apisign": apisign
        }

        print(url)
        return requests.get(url, headers=headers).json()

    # public
    def get_markets(self):
        """ Used to get the open and available trading markets at Bittrex
        along with other meta data.

        Endpoint:
            /public/getmarkets

        Returns:
            JSON
        """
        return self.query_engine('getmarkets')

    def get_currencies(self):
        """Used to get all supported currencies at Bittrex along with other meta data.

        Endpoint:
            /public/getcurrencies

        Returns:
            JSON
        """
        return self.query_engine('getcurrencies')

    def get_ticker(self, market):
        """Used to get the current tick values for a market.

        Endpoint:
            /public/getticker

        Args:
            market (string): string literal for the market (ex: BTC-LTC)

        Returns:
            JSON
        """
        return self.query_engine('getticker', options={"market": market})

    def get_market_summaries(self):
        """Used to get the last 24 hour summary of all active exchanges

        Endpoint:
            /public/getmarketsummaries

        Returns:
            JSON
        """
        return self.query_engine('getmarketsummaries')

    def get_market_summary(self, market):
        """ Used to get the last 24 hour summary of all active exchanges

        Endpoint:
            /public/getmarketsummary

        Args:
            market (string): string literal for the market (ex: BTC-LTC)

        Returns:
            JSON
        """
        return self.query_engine('getmarketsummary', options={"market": market})

    def get_order_book(self, market, type):
        """Used to get retrieve the orderbook for a given market

        Endpoint:
            /public/getorderbook

        Args:
            market (string): string literal for the market (ex: BTC-LTC)
            type (string): buy, sell or both to identify the type of orderbook to return.

        Returns:
            JSON

        """
        return self.query_engine('getorderbook', options={"market": market, "type": type})

    def get_market_history(self, market):
        """Used to retrieve the latest trades that have occured for a specific market.

        Endpoint:
            /public/getmarkethistory

        Args:
            market (string): string literal for the market (ex: BTC-LTC)

        Returns:
            JSON
        """
        return self.query_engine('getmarkethistory', options={"market": market})

    # market
    def buy_limit(self, market, quantity, rate):
        """Used to place a buy order in a specific market.

        Endpoint:
            /market/buylimit

        Args:
            market (string): string literal for the market (ex: BTC-LTC)
            quantity (int): the amount to purchase
            rate (int): the rate at which to place the order

        Returns:
            JSON

        """

        return self.query_engine('buylimit', options={
            "market": market,
            "quantity": quantity,
            "rate": rate,
        })

    def sell_limit(self, market, quantity, rate):
        """Used to place an sell order in a specific market.

        Endpoint:
            /market/selllimit

        Args:
            market (string): string literal for the market (ex: BTC-LTC)
            quantity (int): the amount to purchase
            rate (int): the rate at which to place the order

        Returns:
            JSON
        """
        return self.query_engine('selllimit', options={
            "market": market,
            "quantity": quantity,
            "rate": rate,
        })

    def cancel(self, uuid):
        """ Used to cancel a buy or sell order.

        Endpoint:
            /market/cancel

        Args:
            uuid (string): uuid of buy or sell order

        Returns:
            JSON
        """

        return self.query_engine('cancel', options={
            "uuid": uuid
        })

    def get_open_orders(self, market=None):
        """Get all orders that you currently have opened. A specific market can be requested

        Endpoint:
            /market/getopenorders

        Args:
            market string literal for the market (ie. BTC-LTC)

        Returns:
            JSON
        """

        return self.query_engine('getopenorders',
                                 {"market": market}if market else None)

    def get_balances(self):
        """ Used to retrieve all balances from your account

        Endpoint:
            /account/getbalances

        Returns:
            JSON

        """

        return self.query_engine('getbalances')

    def get_balance(self, currency):
        """ Used to retrieve the balance from your account for a specific currency.

        Endpoint:
            /account/getbalance

        Args:
            currency (string): string literal for the currency (ie. BTC)

        Returns:
            JSON

        """

        return self.query_engine('getbalance', options={
            "currency": currency
        })

    def get_deposit_address(self, currency):
        """ Used to retrieve or generate an address for a specific currency.
        If one does not exist, the call will fail and return ADDRESS_GENERATING
        until one is available.

        Endpoint:
            /account/getdepositaddress

        Args:
            currency (string): string literal for the currency (ie. BTC)

        Returns:
            JSON
        """
        return self.query_engine('getdepositaddress', options={
            "currency": currency
        })

    def withdraw(self, currency, quantity, address):
        """ Used to withdraw funds from your account. note: please account for txfee.

        Endpoint:
            /account/withdraw

        Args:
            currency (string): a string literal for the currency (ie. BTC)
            quantity (int): the quantity of coins to withdraw
            address (string): the address where to send the funds.

        Returns:
            JSON

        """
        return self.query_engine('withdraw', options={
            "currency": currency,
            "quantity": quantity,
            "address": address
        })

    def get_order(self, uuid):
        """ Used to retrieve a single order by uuid.

        Endpoint:
            /account/getorder

        Args:
            uuid (string): uuid of the buy or sell order

        Returns:
            JSON

        """
        return self.query_engine('withdraw', options={
            "uuid": uuid
        })

    def get_order_history(self, market=None):
        """ Used to retrieve your order history.

        Endpoint:
            /account/getorderhistory

        Args:
            market (string) [optional]: a string literal for the market 
            (ie. BTC-LTC). If ommited, will return for all markets

        Returns:
            JSON
        """
        return self.query_engine('getorderhistory',
                                 {"market": market} if market else None)

    def get_withdrawal_history(self, currency=None):
        """ Used to retrieve your withdrawal history. 

        Endpoint:
            /account/getwithdrawalhistory 

        Args:
            currency (string) [optional]:optional a string literal for 
            the currecy (ie. BTC). If omitted, will return for all currencies 

        Returns:
            JSON
        """

        return self.query_engine('getwithdrawalhistory',
                                 {"currency": currency} if currency else None)

    def get_deposit_history(self, currency=None):
        """ Used to retrieve your deposit history.

        Endpoint:
            /account/getdeposithistory 

        Args:
            currency (string) [optional]:optional a string literal for 
            the currecy (ie. BTC). If omitted, will return for all currencies 

        Returns:
            JSON
        """

        return self.query_engine('getdeposithistory',
                                 {"currency": currency} if currency else None)

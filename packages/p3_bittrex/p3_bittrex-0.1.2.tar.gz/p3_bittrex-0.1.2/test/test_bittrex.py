"""
    Requires Bittrex API to be up
    Requires setting env variables for client and secret key
"""

import unittest
import json
import os
from p3_bittrex.p3_bittrex import Bittrex


def test_basic_response(unit_test, result, method_name):
    unit_test.assertTrue(result['success'], "{0:s} failed".format(method_name))
    unit_test.assertTrue(result['message'] is not None,
                         "message not present in response")
    unit_test.assertTrue(result['result'] is not None,
                         "result not present in response")


def test_failed_response(unit_test, result, test_type):
    unit_test.assertFalse(result['success'], "{0:s} failed".format(test_type))
    unit_test.assertTrue(any(x in result['message'].lower() for x in ['exist', 'invalid']),
                         "{0:s} failed response message".format(test_type))
    unit_test.assertIsNone(result['result'],
                           "failed result in response")


def test_response_structure(unit_test, result, method_name):
    unit_test.assertTrue('success' in result, 'Invalid structure')
    unit_test.assertTrue('message' in result, 'Invalid structure')
    unit_test.assertTrue('result' in result, 'Invalid structure')


class TestBittrexPublicAPI(unittest.TestCase):
    """
        Integration tests for Bittrex Public API
    """

    def setUp(self):
        self.bittrex = Bittrex()

    def test_get_markets(self):
        actual = self.bittrex.get_markets()
        test_basic_response(self, actual, 'get_markets')

    def test_get_currencies(self):
        actual = self.bittrex.get_currencies()
        test_basic_response(self, actual, 'get_currencies')

    def test_get_ticker(self):
        self.assertRaises(TypeError, self.bittrex.get_ticker)
        actual = self.bittrex.get_ticker('BTC-LTC')
        test_basic_response(self, actual, 'get_ticker')
        false_actual = self.bittrex.get_ticker('BTC')
        test_failed_response(self, false_actual, 'get_ticker')

    def test_get_market_summaries(self):
        actual = self.bittrex.get_market_summaries()
        test_basic_response(self, actual, 'get_market_summaries')

    def test_get_market_summary(self):
        self.assertRaises(TypeError, self.bittrex.get_market_summary)
        actual = self.bittrex.get_ticker('BTC-LTC')
        test_basic_response(self, actual, 'get_market_summar')
        false_actual = self.bittrex.get_ticker('BTC')
        test_failed_response(self, false_actual, 'get_market_summar')

    def test_get_order_book(self):
        self.assertRaises(TypeError, self.bittrex.get_order_book)
        self.assertRaises(TypeError, self.bittrex.get_order_book, 'BTC-LTC')
        actual = self.bittrex.get_order_book('BTC-LTC', 'buy')
        test_basic_response(self, actual, 'get_order_book')

    def test_get_market_history(self):
        self.assertRaises(TypeError, self.bittrex.get_market_history)
        actual = self.bittrex.get_market_history('BTC-LTC')
        test_basic_response(self, actual, 'get_market_history')


class TestBittrexMarketAPI(unittest.TestCase):

    def setUp(self):
        self.bittrex = Bittrex()

    def test_secret_and_key(self):
        try:
            os.environ['BITTREX_KEY']
            os.environ['BITTREX_SECRET']
        except KeyError:
            self.fail("Requires BITTREX_KEY and BITTREX_SECRET env variables")

    def test_buy_limit(self):
        self.assertRaises(TypeError, self.bittrex.buy_limit)
        actual = self.bittrex.buy_limit('BTC-LTC', 1, 1)
        test_response_structure(self, actual, 'buy_limit')

    def test_sell_limit(self):
        self.assertRaises(TypeError, self.bittrex.buy_limit)
        actual = self.bittrex.sell_limit('BTC-LTC', 1, 1)
        test_response_structure(self, actual, 'sell_limit')

    def test_cancel(self):
        self.assertRaises(TypeError, self.bittrex.cancel)
        # provide invalid uuid but test the json structure
        actual = self.bittrex.cancel('BTC-LTC')
        test_response_structure(self, actual, 'cancel')

    def test_open_orders(self):
        invalid_actual = self.bittrex.get_open_orders('Invalid Market')
        no_param_actual = self.bittrex.get_open_orders()
        actual = self.bittrex.get_open_orders('BTC-LTC')
        test_failed_response(self, invalid_actual, 'get_open_orders')
        test_basic_response(self, no_param_actual, 'get_open_orders')
        test_basic_response(self, actual, 'get_open_orders')


class TestBittrexAccountAPI(unittest.TestCase):

    def setUp(self):
        self.bittrex = Bittrex()

    def test_get_balances(self):
        actual = self.bittrex.get_balances()
        test_basic_response(self, actual, 'get_balances')

    def test_get_balance(self):
        self.assertRaises(TypeError, self.bittrex.get_balance)
        actual = self.bittrex.get_balance('BTC')
        test_basic_response(self, actual, 'get_balance')
        invalid_actual = self.bittrex.get_balance('Invalid currency')
        test_failed_response(self, invalid_actual, 'get_balance')

    def test_get_deposit_address(self):
        self.assertRaises(TypeError, self.bittrex.get_deposit_address)
        actual = self.bittrex.get_deposit_address('BTC')
        test_basic_response(self, actual, 'get_deposit_address')
        invalid_actual = self.bittrex.get_deposit_address('Invalid currency')
        test_failed_response(self, invalid_actual, 'get_deposit_address')

    def test_withdraw(self):
        self.assertRaises(TypeError, self.bittrex.withdraw)

    def test_get_order(self):
        self.assertRaises(TypeError, self.bittrex.get_order)
        actual = self.bittrex.get_order('test')
        test_response_structure(self, actual, 'get_order')

    def test_get_order_history(self):
        actual = self.bittrex.get_order_history()
        test_basic_response(self, actual, 'get_order_history')
        actual = self.bittrex.get_order_history('BTC-LTC')
        test_basic_response(self, actual, 'get_order_history')

    def test_get_withdrawal_historyself(self):
        actual = self.bittrex.get_withdrawal_history()
        test_basic_response(self, actual, 'get_withdrawal_history')
        actual = self.bittrex.get_withdrawal_history('BTC')
        test_basic_response(self, actual, 'get_withdrawal_history')

    def test_get_deposit_history(self):
        actual = self.bittrex.get_deposit_history()
        test_basic_response(self, actual, 'get_deposit_history')
        actual = self.bittrex.get_deposit_history('BTC')
        test_basic_response(self, actual, 'get_deposit_history')


if __name__ == '__main__':
    unittest.main()

import unittest
from src.trader.trader import Trader

class TestTrader(unittest.TestCase):

    # Test a successfull buy.
    def test_trader_buy(self):
        initial_funds = 100.0
        trader = Trader(initial_funds)
        trader.buy("coin", 60)

        self.assertEqual(trader.funds, 40.0)
        self.assertEqual(trader.assets, {"coin": 1})

    # Test a successfull buy and then a successfull sell.
    def test_trader_successful_sell(self):
        initial_funds = 100.0
        trader = Trader(initial_funds)
        trader.buy("coin", 60)
        trader.sell("coin", 40)

        self.assertEqual(trader.funds, 80.0)
        self.assertEqual(trader.assets, {"coin": 0})

    # Test you can not sell before have bought anything.
    def test_not_sell_before_buy(self):
        initial_funds = 100.0
        trader = Trader(initial_funds)
        trader.sell("coin", 60)
        self.assertEqual(trader.funds, 100.0)
        self.assertEqual(trader.assets, {})

if __name__ == '__main__':
    unittest.main()
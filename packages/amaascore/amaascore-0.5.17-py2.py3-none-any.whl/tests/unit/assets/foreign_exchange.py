from __future__ import absolute_import, division, print_function, unicode_literals

from decimal import Decimal
import random
import unittest

from amaascore.assets.foreign_exchange import ForeignExchange, ForeignExchangeForward, ForeignExchangeSpot
from amaascore.assets.interface import AssetsInterface
from amaascore.tools.generate_asset import generate_foreignexchange, generate_fx_forward, generate_fx_spot


class ForeignExchangeTest(unittest.TestCase):

    def setUp(self):
        self.longMessage = True  # Print complete error message on failure
        self.asset_manager_id = random.randint(1, 2**31-1)
        self.fx_forward = generate_fx_forward(asset_manager_id=self.asset_manager_id)
        self.asset_id = self.fx_forward.asset_id
        self.assets_interface = AssetsInterface()

    def tearDown(self):
        pass

    def test_ForeignExchange(self):
        fx = generate_foreignexchange(asset_id='USDJPY')
        self.assertEqual(type(fx), ForeignExchange)

    def test_ForeignExchangeForward(self):
        self.assertEqual(type(self.fx_forward), ForeignExchangeForward)

    def test_ForeignExchangeSpot(self):
        fx_spot = generate_fx_spot(asset_manager_id=self.asset_manager_id)
        self.assertEqual(type(fx_spot), ForeignExchangeSpot)

    def test_Persistence(self):
        self.assets_interface.new(self.fx_forward)
        fx_forward = self.assets_interface.retrieve(asset_manager_id=self.asset_manager_id, asset_id=self.asset_id)
        self.assertEqual(fx_forward, self.fx_forward)

if __name__ == '__main__':
    unittest.main()

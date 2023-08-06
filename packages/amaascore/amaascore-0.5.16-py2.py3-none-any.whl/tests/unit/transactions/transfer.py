# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from decimal import Decimal
import random
import unittest

from amaascore.transactions.interface import TransactionsInterface
from amaascore.transactions.transaction import Transaction
from amaascore.tools.generate_asset import generate_asset
from amaascore.tools.generate_book import generate_book
from amaascore.tools.generate_transaction import generate_transaction


class TransferTest(unittest.TestCase):

    def setUp(self):
        self.longMessage = True  # Print complete error message on failure
        self.maxDiff = None  # View the complete diff when there is a mismatch in a test
        self.interface = TransactionsInterface()
        self.asset_manager_id = random.randint(1, 2**31-1)
        self.asset = generate_asset(asset_manager_id=self.asset_manager_id, fungible=True)
        self.trader_one_book = generate_book(asset_manager_id=self.asset_manager_id)
        self.trader_two_book = generate_book(asset_manager_id=self.asset_manager_id)
        self.wash_book = generate_book(asset_manager_id=self.asset_manager_id)
        self.setup_cache()

    def setup_cache(self):
        self.create_transaction_asset()
        self.create_transaction_book(self.trader_one_book)
        self.create_transaction_book(self.trader_two_book)
        self.create_transaction_book(self.wash_book)

    def tearDown(self):
        pass

    def create_transaction_asset(self):
        transaction_asset_fields = ['asset_manager_id', 'asset_id', 'asset_status', 'asset_class', 'asset_type',
                                    'fungible']
        asset_json = self.asset.to_json()
        transaction_asset_json = {attr: asset_json.get(attr) for attr in transaction_asset_fields}
        self.interface.upsert_transaction_asset(transaction_asset_json=transaction_asset_json)

    def create_transaction_book(self, book):
        transaction_book_fields = ['asset_manager_id', 'book_id', 'party_id', 'book_status']
        book_json = book.to_json()
        transaction_book_json = {attr: book_json.get(attr) for attr in transaction_book_fields}
        self.interface.upsert_transaction_book(transaction_book_json=transaction_book_json)

    def test_BookTransfer(self):
        deliver, receive = self.interface.book_transfer(asset_manager_id=self.asset_manager_id,
                                                        source_book_id=self.trader_one_book.book_id,
                                                        target_book_id=self.trader_two_book.book_id,
                                                        wash_book_id=self.wash_book.book_id,
                                                        asset_id=self.asset.asset_id,
                                                        quantity=100,
                                                        price=Decimal('3.14'),
                                                        currency='USD')
        self.assertEqual(deliver.quantity, 100)
        self.assertEqual(receive.quantity, 100)
        self.assertEqual(deliver.transaction_action, 'Deliver')
        self.assertEqual(receive.transaction_action, 'Receive')
        self.assertEqual(deliver.transaction_type, 'Transfer')
        self.assertEqual(deliver.transaction_type, 'Transfer')
        self.assertEqual(deliver.counterparty_book_id, self.wash_book.book_id)
        self.assertEqual(receive.counterparty_book_id, self.wash_book.book_id)

if __name__ == '__main__':
    unittest.main()

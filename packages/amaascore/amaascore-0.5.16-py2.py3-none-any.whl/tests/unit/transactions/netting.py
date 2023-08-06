# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from decimal import Decimal
import unittest

from amaascore.transactions.interface import TransactionsInterface
from amaascore.transactions.transaction import Transaction
from amaascore.tools.generate_asset import generate_asset
from amaascore.tools.generate_book import generate_book
from amaascore.tools.generate_transaction import generate_transaction


class NettingTest(unittest.TestCase):

    def setUp(self):
        self.longMessage = True  # Print complete error message on failure
        self.maxDiff = None  # View the complete diff when there is a mismatch in a test
        self.interface = TransactionsInterface()
        self.asset_manager_id = 1
        self.asset = generate_asset(asset_manager_id=self.asset_manager_id, fungible=True)
        self.asset_book = generate_book(asset_manager_id=self.asset_manager_id)
        self.counterparty_book = generate_book(asset_manager_id=self.asset_manager_id)
        self.transaction1 = generate_transaction(asset_manager_id=self.asset_manager_id, asset_id=self.asset.asset_id,
                                                 asset_book_id=self.asset_book.book_id,
                                                 counterparty_book_id=self.counterparty_book.book_id,
                                                 transaction_currency='USD',
                                                 net_affecting_charges=True,
                                                 charge_currency='USD')
        self.transaction2 = generate_transaction(asset_manager_id=self.asset_manager_id, asset_id=self.asset.asset_id,
                                                 asset_book_id=self.asset_book.book_id,
                                                 counterparty_book_id=self.counterparty_book.book_id,
                                                 transaction_currency='USD',
                                                 net_affecting_charges=True,
                                                 charge_currency='USD')
        self.setup_cache()
        self.interface.new(self.transaction1)
        self.interface.new(self.transaction2)
        self.transaction_id1 = self.transaction1.transaction_id
        self.transaction_id2 = self.transaction2.transaction_id

    def tearDown(self):
        pass

    def create_transaction_asset(self):
        transaction_asset_fields = ['asset_manager_id', 'asset_id', 'asset_status', 'asset_class', 'asset_type',
                                    'fungible']
        asset_json = self.asset.to_json()
        transaction_asset_json = {attr: asset_json.get(attr) for attr in transaction_asset_fields}
        self.interface.upsert_transaction_asset(transaction_asset_json=transaction_asset_json)

    def setup_cache(self):
        self.create_transaction_asset()
        self.create_transaction_book(self.asset_book)
        self.create_transaction_book(self.counterparty_book)

    def create_transaction_book(self, book):
        transaction_book_fields = ['asset_manager_id', 'book_id', 'party_id', 'book_status']
        book_json = book.to_json()
        transaction_book_json = {attr: book_json.get(attr) for attr in transaction_book_fields}
        self.interface.upsert_transaction_book(transaction_book_json=transaction_book_json)

    def test_GenerateNettingSet(self):
        net = self.interface.net_transactions(asset_manager_id=self.asset_manager_id,
                                              transaction_ids=[self.transaction_id1, self.transaction_id2])
        self.assertEqual(type(net), Transaction)
        transaction_ids = {link.linked_transaction_id for link in net.links.get('NettingSet')}
        self.assertEqual(transaction_ids, {self.transaction_id1, self.transaction_id2})

    def test_RetrieveNettingSet(self):
        net = self.interface.net_transactions(asset_manager_id=self.asset_manager_id,
                                              transaction_ids=[self.transaction_id1, self.transaction_id2])
        net_transaction_id, netting_set = self.interface.retrieve_netting_set(asset_manager_id=self.asset_manager_id,
                                                                              transaction_id=net.transaction_id)
        self.assertEqual(net_transaction_id, net.transaction_id)
        self.assertEqual(len(netting_set), 2)
        transaction_ids = {transaction.transaction_id for transaction in netting_set}
        self.assertEqual(transaction_ids, {self.transaction_id1, self.transaction_id2})

if __name__ == '__main__':
    unittest.main()

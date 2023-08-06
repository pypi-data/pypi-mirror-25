from __future__ import absolute_import, division, print_function, unicode_literals

from amaasutils.logging_utils import DEFAULT_LOGGING
import random
import unittest

from amaascore.asset_managers.asset_manager import AssetManager
from amaascore.asset_managers.interface import AssetManagersInterface
from amaascore.asset_managers.relationship import Relationship
from amaascore.tools.generate_asset_manager import generate_asset_manager, generate_relationship

import logging.config
logging.config.dictConfig(DEFAULT_LOGGING)


class AssetManagersInterfaceTest(unittest.TestCase):

    def setUp(self):
        self.longMessage = True  # Print complete error message on failure
        self.asset_managers_interface = AssetManagersInterface()
        self.asset_manager_id = random.randint(1, 2**31-1)
        self.related_id = random.randint(1, 2**31-1)

    def tearDown(self):
        pass

    def test_New(self):
        asset_manager = generate_asset_manager()
        asset_manager = self.asset_managers_interface.new(asset_manager)
        self.assertEqual(type(asset_manager), AssetManager)

    def test_Amend(self):
        asset_manager = generate_asset_manager()
        asset_manager = self.asset_managers_interface.new(asset_manager)
        self.assertEqual(type(asset_manager), AssetManager)

    def test_SearchAndRetrieve(self):
        all_asset_managers = self.asset_managers_interface.search()
        random_index = random.randint(0, len(all_asset_managers)-1)
        asset_manager = all_asset_managers[random_index]
        retrieved_manager = self.asset_managers_interface.retrieve(asset_manager_id=asset_manager.asset_manager_id)
        self.assertEqual(retrieved_manager, asset_manager)

    def test_NewRelationship(self):
        asset_manager = generate_asset_manager(asset_manager_id=self.asset_manager_id)
        self.asset_managers_interface.new(asset_manager)
        relation = generate_asset_manager(asset_manager_id=self.related_id)
        self.asset_managers_interface.new(relation)
        relationship = generate_relationship(asset_manager_id=self.asset_manager_id,
                                             related_id=self.related_id)
        relationship = self.asset_managers_interface.new_relationship(relationship)
        self.assertEqual(type(relationship), Relationship)

    def test_AmendRelationship(self):
        asset_manager = generate_asset_manager(asset_manager_id=self.asset_manager_id)
        self.asset_managers_interface.new(asset_manager)
        relation = generate_asset_manager(asset_manager_id=self.related_id)
        self.asset_managers_interface.new(relation)
        relationship = generate_relationship(asset_manager_id=self.asset_manager_id,
                                             related_id=self.related_id,
                                             relationship_type='External')
        relationship = self.asset_managers_interface.new_relationship(relationship)
        relationship.relationship_type = 'Employee'
        relationship = self.asset_managers_interface.amend_relationship(relationship)
        self.assertEqual(type(relationship), Relationship)

    def test_RetrieveRelationship(self):
        asset_manager = generate_asset_manager(asset_manager_id=self.asset_manager_id)
        self.asset_managers_interface.new(asset_manager)
        relation = generate_asset_manager(asset_manager_id=self.related_id)
        self.asset_managers_interface.new(relation)
        relationship = generate_relationship(asset_manager_id=self.asset_manager_id,
                                             related_id=self.related_id,
                                             relationship_type='External')
        relationship = self.asset_managers_interface.new_relationship(relationship)
        relationship.relationship_type = 'Employee'
        self.asset_managers_interface.amend_relationship(relationship)
        relations = self.asset_managers_interface.retrieve_relationships(asset_manager_id=self.asset_manager_id)
        self.assertEqual(len(relations), 1)
        self.assertEqual(type(relations[0]), Relationship)
        self.assertEqual(relations[0].relationship_type, 'Employee')

if __name__ == '__main__':
    unittest.main()

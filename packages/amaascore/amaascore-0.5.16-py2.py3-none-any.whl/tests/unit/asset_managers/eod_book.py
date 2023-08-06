from __future__ import absolute_import, division, print_function, unicode_literals

import unittest
from datetime import datetime
from amaascore.tools.generate_asset_manager import generate_eod_book


class AssetManagerTest(unittest.TestCase):

    def setUp(self):
        self.longMessage = True  # Print complete error message on failure
        self.utc_close_time = datetime.utcnow().time()
        self.eod_book = generate_eod_book(utc_close_time=self.utc_close_time)

    def tearDown(self):
        pass

    def testStatus(self):
        self.assertEqual(self.eod_book.eod_book_status, 'Active')
    
    def testUtcCloseTime(self):
        expected = self.utc_close_time.strftime('%H:%M:%S')
        self.assertEqual(self.eod_book.utc_close_time, expected)

if __name__ == '__main__':
    unittest.main()

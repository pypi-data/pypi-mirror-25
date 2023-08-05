import unittest
from service import utils

class IdGeneratorTest(unittest.TestCase):

    def setUp(self):
        utils.IdGenerator.setup({"global": -1, "cat1": 1000})

    def tearDown(self):
        pass

    def test_get_next(self):
        self.assertEqual(utils.IdGenerator.next(), 0)
        self.assertEqual(utils.IdGenerator.next(), 1)
        self.assertEqual(utils.IdGenerator.next("cat1"), 1001)

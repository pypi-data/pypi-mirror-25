import unittest


class PackageScanTest(unittest.TestCase):

    repo = None

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_scan(self):
        m = __import__("persist.beans", fromlist=("persist"))
        d = getattr(m, "beans")
        self.assertTrue(isinstance(d, dict))

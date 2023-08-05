from domain import exceptions
import unittest

class ExceptionsTest(unittest.TestCase):

    repo = None

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_exceptions(self):
        nf = exceptions.NotFoundException("record not found : aaa")
        print(nf)
        self.assertEqual(nf.err_code, 1001)

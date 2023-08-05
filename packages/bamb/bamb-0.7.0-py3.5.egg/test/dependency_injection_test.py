import bamb
import unittest
from domain import base
from bson.objectid import ObjectId
from domain import exceptions
from bamb import Bamb
from common import constants
from domain import task

class DependencyInjectionTest(unittest.TestCase):

    repo = None

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load(self):
        app = Bamb.singleton()
        ts = app.get_bean(constants.SERVICE_TASK)
        t = task.Task("task 1")
        ts.save(t, key="43043920F2038193D1C8010C")
        t1 = ts.load("43043920F2038193D1C8010C")
        self.assertEqual(t1.name, "task 1")

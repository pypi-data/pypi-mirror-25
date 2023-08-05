import bamb
import unittest
from domain import base
from bson.objectid import ObjectId
from domain import exceptions
from persist import simple_repository



class Foo(base.EasySerializable, base.ListTree):

    def __init__(self, name="", key=0):
        self.key = key
        self.name = name
        base.EasySerializable.__init__(self)
        base.ListTree.__init__(self)

class FooRepo(simple_repository.SimpleMongoDbRepository):

    def __init__(self):
        simple_repository.SimpleMongoDbRepository.__init__(self, bamb.Bamb.singleton())

    @property
    def table_name(self):
        return "foo"

class MongoDbTest(unittest.TestCase):

    repo = None

    def setUp(self):
        MongoDbTest.repo = FooRepo()

    def tearDown(self):
        pass

    def test_save(self):
        f = self.build_object()
        i = ObjectId("A203EFCD023942A203EFCD02")
        r = MongoDbTest.repo
        result = r.save(f, key=i)
        print(result)
        o = r.load(result)
        self.assertTrue(isinstance(o, base.EasySerializable))


    def test_update(self):
        f = self.build_object()
        i = ObjectId("A203EFCD023942A203EFCD02")
        r = MongoDbTest.repo
        result = r.save(f, key=i)
        o = r.load(result)
        self.assertTrue(isinstance(o, base.EasySerializable))
        o.child([1, 1]).name = "h900p"
        result = r.save(o)
        p = r.load(result)
        self.assertEqual(p.child([1,1]).name, "h900p")
        i = ObjectId("B203EFCDD23952A20800AE53")
        with self.assertRaises(exceptions.NotFoundException) as cm:

            result = r.update(o, key=i, upsert=False)

        ex = cm.exception
        self.assertTrue(ex is not None)

    def test_update_partial(self):
        f = self.build_object()
        i = ObjectId("A203EFCD023942A203EFCD02")
        r = MongoDbTest.repo
        result = r.save(f, key=i)
        o = r.load("A203EFCD023942A203EFCD02[1,0]")
        self.assertTrue(isinstance(o, base.EasySerializable))
        self.assertEqual(o.name, "foo2.1")
        o = r.load("A203EFCD023942A203EFCD02")
        o = o.child([1,0])
        o.name = "h900p"
        r.save(o)
        o = r.load("A203EFCD023942A203EFCD02[1,0]")
        self.assertEqual(o.name, "h900p")

    def build_object(self):

        f = Foo("foo", 1)
        f1 = Foo("foo1", 10)
        f11 = Foo("foo1.1", 11)
        f12 = Foo("foo1.2", 12)
        f2 = Foo("foo2",20)
        f21 = Foo("foo2.1", 21)
        f22 = Foo("foo2.2", 22)
        f1.lt_add_child(f12)
        f1.lt_insert_child(f11, 0)
        f2.lt_add_child(f21)
        f2.lt_insert_child(f22, -1)
        f.lt_extend_children([f1, f2])
        f3 = Foo("foo3", 30)
        f3.lt_extend_children([Foo("foo3.1", 31), Foo("foo3.2", 32), Foo("foo3.3", 33), Foo("foo3.4", 34), Foo("foo3.5", 35)])
        f.lt_add_child(f3)

        return f

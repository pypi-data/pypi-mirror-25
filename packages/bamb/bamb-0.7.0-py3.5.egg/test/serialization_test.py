import unittest
from domain import base


class Dummy(object):
    pass


class Foo(base.EasySerializable):

    def __init__(self, original_dict={}, name=""):
        super(Foo, self).__init__(original_dict, name)
        if not self.es_dict_updated:
            self.children = []
            self.dummy = Dummy()
            self.dummy1 = None
            self.name = name
            self.keyed_children = {}

    @property
    def dwi(self):
        return [["dummy"]]


class SerializationTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_decorator_creation(self):
        f = Foo()
        self.assertTrue(isinstance(f, base.EasySerializable))
        self.assertTrue(isinstance(f, Foo))

    def test_to_dict(self):
        f = Foo(name="foo")
        d = f.es_to_dict()
        self.assertTrue(len(d) > 0)
        print("instance of Foo to dict : ", d)
        self.assertEqual(d.get("name"), "foo")
        self.assertEqual(d.get("dummy", "nothing"), "nothing")

    def test_load_by_method(self):
        f = Foo(name="foo")
        d = f.es_to_dict()
        f1 = base.EasySerializable.es_load(d)
        self.assertTrue(isinstance(f1, Foo))
        self.assertTrue(f1.name, f.name)

    def test_load_by_constructor(self):
        f = Foo(name="foo")
        d = f.es_to_dict()
        f1 = Foo(original_dict=d)
        self.assertTrue(isinstance(f1, Foo))
        self.assertTrue(f1.name, f.name)

    def test_to_dict_mass(self):
        f = self.build_mass_object()
        d = f.es_to_dict()
        self.assertTrue(len(d) > 0)
        print("instance of Foo to dict(mass) : ", d)
        fl1 = d.get("children")
        self.assertEqual(len(fl1), 3)
        fl3 = fl1[2].get("keyed_children")
        self.assertEqual(len(fl3), 2)

    def test_load_by_method_mass(self):
        f = self.build_mass_object()
        d = f.es_to_dict()
        f1 = base.EasySerializable.es_load(d)
        self.assertTrue(isinstance(f1, Foo))
        self.assertTrue(f1.name, f.name)
        self.assertEqual(len(f1.children), 3)
        self.assertEqual(len(f1.children[2].keyed_children), 2)

    def build_mass_object(self):
        f = Foo(name="foo")
        f1 = Foo(name="foo1")
        f1.children.append(Foo(name="foo1.1"))
        f.children.append(f1)
        f.children.append(Foo(name="foo2"))
        f3 = Foo(name="foo3")
        f3.keyed_children["foo3.1"] = Foo(name="foo3.1")
        f3.keyed_children["foo3.2"] = Foo(name="foo3.2")
        f.children.append(f3)
        return f


import unittest
from domain import base


class Foo(base.EasySerializable, base.ListTree):

    def __init__(self, name=""):
        self.name = name
        base.EasySerializable.__init__(self)
        base.ListTree.__init__(self)

    @staticmethod
    def name_matcher(f1, f2):
        if not isinstance(f1, Foo):
            return False
        if not isinstance(f2, Foo1):
            return False
        return f1.name == f2.name


class Foo1(base.EasySerializable, base.ListTree):

    def __init__(self, name=""):
        self.name = name
        base.EasySerializable.__init__(self)
        base.ListTree.__init__(self)


class ListTreeTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_index(self):
        f = self.build_object()
        d = f.es_to_dict()
        self.do_test_for_a_typical_object(f)
        f1 = base.EasySerializable.es_load(d)
        self.do_test_for_a_typical_object(f1)

    def do_test_for_a_typical_object(self, f):

        self.assertEqual(f.child("0.1").name, "foo1.2")
        self.assertEqual(f.child("0.1").lt_path(), [0, 1])
        f21 = f.child("1.0")

        self.assertEqual(f21.name, "foo2.1")
        self.assertEqual(f21.lt_parent.name, "foo2")
        self.assertEqual(f21.lt_root().name, "foo")
        self.assertEqual(f.child([]).name, "foo")

        f22 = f.child("1.1")
        f1 = f.child([0])
        f.lt_remove([1, 0])
        self.assertEqual(f22.lt_path(), [1, 0])
        f1.lt_remove()
        self.assertEqual(f22.lt_path(), [0, 0])

    def test_leaf_related_functions(self):

        f = self.build_object()
        leaves = f.get_all_leaves()
        self.assertEqual(len(leaves), 9)
        self.assertEqual(leaves[4].name, "foo3.1")
        self.assertEqual(f.child("0").lt_next().name, "foo2.1")
        leaves = f.get_all_leaves(reverse=True)
        self.assertEqual(len(leaves), 9)
        self.assertEqual(leaves[5].name, "foo2.2")
        self.assertTrue(f.child("0").lt_prev() is None)
        self.assertEqual(f.child("1").lt_prev().name, "foo1.2")

    def test_copy(self):

        f = self.build_object()
        f1 = self.build_objects_respondingly()
        ff = f.lt_copy(Foo.name_matcher, f1)
        self.assertEqual(len(ff.child("0").lt_children), 1)
        self.assertEqual(ff.child("1.1").name, "foo3.2")
        self.assertEqual(ff.child("1.3").name, "foo3.5")

    def test_yield(self):

        f = self.build_object()
        it = []

        for i in f.lt_iterator():
            print(i.name)
            it.append(i)

        self.assertEqual(len(it), 13)

    @staticmethod
    def always_true_matcher(o):
        return True

    def build_object(self):

        f = Foo("foo")
        f1 = Foo("foo1")
        f11 = Foo("foo1.1")
        f12 = Foo("foo1.2")
        f2 = Foo("foo2")
        f21 = Foo("foo2.1")
        f22 = Foo("foo2.2")
        f1.lt_add_child(f12)
        f1.lt_insert_child(f11, 0)
        f2.lt_add_child(f21)
        f2.lt_insert_child(f22, -1)
        f.lt_extend_children([f1, f2])
        f3 = Foo("foo3")
        f3.lt_extend_children([Foo("foo3.1"), Foo("foo3.2"), Foo("foo3.3"), Foo("foo3.4"), Foo("foo3.5")])
        f.lt_add_child(f3)

        return f

    def build_objects_respondingly(self):

        f = Foo1("foo")
        f1 = Foo1("foo1")
        f11 = Foo1("foo1.1")
        f2 = Foo1("kkk2")
        f21 = Foo1("foo2.1")
        f22 = Foo1("foo2.2")
        f1.lt_insert_child(f11, 0)
        f2.lt_add_child(f21)
        f2.lt_insert_child(f22, -1)
        f.lt_extend_children([f1, f2])
        f3 = Foo1("foo3")
        f3.lt_extend_children([Foo1("foo3.1"), Foo1("foo3.2"), Foo1("foo3.3"), Foo1("kkk3.4"), Foo1("foo3.5")])
        f.lt_add_child(f3)

        return f
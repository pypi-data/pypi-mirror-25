from unittest import TestCase

from april.tipes import listof, setof, tupleof
from april import Model


class TestListof(TestCase):

    def test_listof(self):
        listof_str = listof(str)
        str_list = ['hello', 'world']
        str_list_new = listof_str(str_list)
        self.assertEqual(str_list, str_list_new)

    def test_listof_2(self):
        """listof initialized with a object which is not a class"""
        listof_str = listof(str)
        self.assertRaises(ValueError, listof_str, [1, 2])

    def test_listof_3(self):
        """when datatype is not a class"""
        self.assertRaises(ValueError, listof, 1)

    def test_listof_4(self):
        """when listof_class initialized with a object which is not a list"""
        listof_str = listof(str)
        self.assertRaises(ValueError, listof_str, 'name')

    def test_isinstance(self):
        listof_str = listof(str)
        self.assertFalse(isinstance(1, listof_str))
        self.assertTrue(isinstance(listof_str(['hello']), listof_str))

    def test_isinstance_2(self):
        class User(Model):
            name = str
        listof_User = listof(User)
        self.assertTrue(isinstance(listof_User([User(name='Tom')]), listof_User))
        self.assertFalse(isinstance([{'name': 'Tom'}], listof_User))

    def test_validate(self):
        listof_str = listof(str)
        self.assertRaises(ValueError, listof_str, 1)


class TestSetOf(TestCase):
    def test_usage(self):
        setof_str = setof(str)
        s = setof_str({'hello', 'world', 'hello'})
        self.assertIn('hello', s)


class TestTupleOf(TestCase):
    def test_usage(self):
        tupleof_str = tupleof(str)
        s = tupleof_str(('hello', 'world', 'hello'))
        self.assertIn('hello', s)
        self.assertTrue(len(s), 3)

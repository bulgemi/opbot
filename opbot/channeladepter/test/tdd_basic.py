# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import unittest


class BasicUsageTest(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])

        with self.assertRaises(TypeError):
            s.split(2)


class BasicMariadbTest(unittest.TestCase):
    def test_connect_db(self):
        import sqlalchemy

        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://opbot_appl:apbot_appl26#!@localhost/opbot_db'
        engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
        print(engine.table_names())


if __name__ == '__main__':
    unittest.main()

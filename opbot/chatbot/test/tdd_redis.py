# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import unittest
import redis


class TestRedis(unittest.TestCase):
    def setUp(self) -> None:
        self.r = redis.Redis(host='localhost', port=6389, db=0)

    def test_001_set(self):
        print(self.r.set('foo', 'bar'))

    def test_002_get(self):
        print(self.r.get('foo'))
        print(self.r.get('koo'))

    def test_003_get_equal(self):
        foo = self.r.get('foo')
        self.assertEqual(foo, b'bar')
        self.assertEqual(foo.decode('utf-8'), 'bar')

    def test_004_set_list(self):
        print(self.r.lpush('loo', 'bar'))
        print(self.r.lpush('loo', 'car'))
        print(self.r.lpush('loo', 'far'))
        # print(self.r.lpush('loo', 'bar', 'car', 'far'))

    def test_005_get_list(self):
        print('-'*20)
        while self.r.llen('loo') != 0:
            loo = self.r.rpop('loo')
            print(loo.decode('utf-8'))
        print('-'*20)

    def test_006_get_list_retry(self):
        print('='*20)
        while self.r.llen('loo') != 0:
            loo = self.r.lpop('loo')
            print(loo.decode('utf-8'))
        print('='*20)

    def test_007_set_hash(self):
        data = {'subject1': 'A'}
        self.r.hmset('subject_#list', data)
        print(self.r.hgetall('subject_#list'))
        print(self.r.hget('subject_#list', 'subject1'))

    def test_008_add_hash(self):
        data = {'subject2': 'S'}
        self.r.hmset('subject_#list', data)
        print(self.r.hgetall('subject_#list'))
        print(self.r.hget('subject_#list', 'subject2'))

    def test_009_del_hash(self):
        self.r.hdel('subject_#list', 'subject2')
        print(self.r.hgetall('subject_#list'))
        print(self.r.hget('subject_#list', 'subject2'))

    def test_010_set_hash_none(self):
        from redis.exceptions import DataError
        try:
            self.r.hmset('subject_#list2', None)
        except DataError as e:
            print(e)

    def test_011_del_hash_none(self):
        print("----->", self.r.hdel('subject_#list', 'subject5'))

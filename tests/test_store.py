# -*- coding: UTF-8 -*-

import platform

if platform.python_version() < '2.7':
    import unittest2 as unittest
else:
    import unittest

# TODO test with a fake Mongo DB and with a real one, created for these tests
import pymongo
from remindme import store

class TestStore(unittest.TestCase):

    def setUp(self):
        self.fake_db = {}
        self._get_db = store.get_db
        self._mongoclient = pymongo.MongoClient

        def fake_get_db():
            return self.fake_db

        def fake_client(*args, **kw):
            return {'remindme': self.fake_db}

        store.get_db = fake_get_db
        pymongo.MongoClient = fake_client

    def tearDown(self):
        store.get_db = self._get_db
        pymongo.MongoClient = self._mongoclient


    def test_connect_db_return_db_obj(self):
        k, v = 'foox1a2z', 'xsa3%d'

        self.fake_db[k] = v
        store.connect_db()
        self.assertIn(k, store.db)
        self.assertEquals(store.db[k], v)

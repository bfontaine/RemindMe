# -*- coding: UTF-8 -*-

import os
import pymongo
from bson.objectid import ObjectId

from werkzeug.security import generate_password_hash, check_password_hash

client = pymongo.MongoClient(host=os.environ.get('MONGO_URL',
                                                 'localhost'))
db = client[os.environ.get('MONGODB_DATABASE', 'remindme')]

class DBObject(object):
    collection = 'main'

    def __init__(self, attrs=None):
        self.__dict__['attrs'] = attrs or {}
        self.__dict__['_coll'] = db[self.collection]

    def __setitem__(self, name, value):
        self.attrs[name] = value

    def __getitem__(self, name):
        return self.attrs.get(name)

    def __setattr__(self, name, value):
        return self.__setitem__(name, value)

    def __getattr__(self, name):
        return self.__getitem__(name)

    def get_id(self):
        return unicode(self.attrs.get('_id'))

    def save(self):
        self._coll.save(self.attrs)

    @staticmethod
    def get_instance(self, uid):
        """
        Retrieve or create an user from its id
        """
        el = db[self.collection].find_one({'_id': uid})
        if el:
            return el
        el = self(_id=uid)
        el.save()
        return el


class User(DBObject):
    collection = 'user'

    def __init__(self, email, password=None, api_username=None,
            api_password=None):
        if password and api_username and api_password:
            super(User, self).__init__({
                'email': email,
                'api_username': api_username,
                'api_password': api_password,
            })
            self.set_password(password)
        else:
            super(User, self).__init__(email) # email is a dict used for attrs

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)


def get_coll(klass):
    """
    Return the collection associated with a class

    >>> coll = get_coll(User)
    """
    return db[klass.collection]


def get_user(**spec):
    """
    Return an user according to a spec

    >>> user = get_user(email='foo@bar.com')
    """

    if '_id' in spec:
        spec['_id'] = ObjectId(spec['_id'])

    attrs = get_coll(User).find_one(spec)
    if attrs:
        return User(attrs)

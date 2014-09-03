# -*- coding: UTF-8 -*-

import os
import pymongo
from bson.objectid import ObjectId

from werkzeug.security import generate_password_hash, check_password_hash

db = None

class DBObject(object):
    collection = 'main'

    def __init__(self, attrs=None):
        connect_db()
        self.__dict__['attrs'] = attrs or {}
        self.__dict__['_coll'] = get_db()[self.collection]

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
        el = self._coll.find_one({'_id': uid})
        if el:
            return el
        el = self(_id=uid)
        el.save()
        return el


class User(DBObject):
    """
    An user. It should have the following fields:
    - email
    - pw_hash
    - api_id
    - api_key
    """

    collection = 'user'

    def __init__(self, email, password=None, api_id=None,
            api_key=None):
        if password and api_id and api_key:
            super(User, self).__init__({
                'email': email,
                'api_id': api_id,
                'api_key': api_key,
            })
            self.set_password(password)
        else:
            super(User, self).__init__(email) # email is a dict used for attrs

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)


class SMS(DBObject):
    """
    An SMS. It should have the following fields:
    - user_id: this will be used to retrieve the user's API credentials
    - text
    - send_on: scheduled date
    """

    collection = 'sms'



def connect_db():
    """
    Populate the global 'db' object.
    """
    global db
    if db is not None:
        return
    client = pymongo.MongoClient(host=os.environ.get('MONGO_URL', 'localhost'))
    db = client[os.environ.get('MONGODB_DATABASE', 'remindme')]


def get_db():
    """
    Return the global 'db' object, ensuring it has been initialized
    """
    global db
    connect_db()
    return db


def get_coll(klass):
    """
    Return the collection associated with a class

    >>> coll = get_coll(User)
    """
    return get_db()[klass.collection]


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


def get_smses(**spec):
    return map(SMS, get_coll(SMS).find(spec))


def del_sms(sms):
    # http://stackoverflow.com/a/23335020/735926
    get_coll(SMS).remove({'_id': sms._id}, safe=True)

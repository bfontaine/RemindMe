# -*- coding: UTF-8 -*-

import platform

if platform.python_version() < '2.7':
    import unittest2 as unittest
else:
    import unittest

# TODO test with a fake Mongo DB and with a real one, created for these tests
from remindme import store

class TestStore(unittest.TestCase):

    pass  # TODO

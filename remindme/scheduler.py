# -*- coding: UTF-8 -*-

from log import logger


def run():
    from store import get_coll, SMS
    # ensure proper indexing
    get_coll(SMS).ensure_index([('send_on', 1)])

    # TODO

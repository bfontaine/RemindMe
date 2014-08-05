# -*- coding: UTF-8 -*-

def run():
    from store import get_coll, SMS
    # ensure proper indexing
    get_coll(SMS).ensure_index({'send_on': 1, 'user_id': 1})

    # TODO

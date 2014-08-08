# -*- coding: UTF-8 -*-

from time import sleep

from log import logger
from sms import send_sms


def run():
    from store import get_coll, SMS
    # ensure proper indexing
    get_coll(SMS).ensure_index([('send_on', 1)])

    logger.info('Starting main scheduling loop')
    while True: # main loop
        pass  # TODO
        sleep(60)

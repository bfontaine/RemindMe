# -*- coding: UTF-8 -*-

from time import sleep
from datetime import datetime, timedelta

from core import send_sms
from log import mkLogger
import store

logger = mkLogger('scheduler')


def run():
    from store import get_coll, SMS
    # ensure proper indexing
    get_coll(SMS).ensure_index([('send_on', 1)])

    one_minute = timedelta(minutes=1)

    logger.info('Starting main scheduling loop')
    while True: # main loop
        logger.debug("I'm awake.")

        now = datetime.utcnow()
        one_minute_later = now + one_minute

        logger.info("Current time: %s." % now)

        uid_cache = {}
        smses = store.get_smses(send_on={'$gte': now, '$lt': one_minute_later})

        smses = list(smses)  # needed to get a length
        logger.info('Got %d SMSes.' % len(smses))

        for sms in smses:
            uid = sms.user_id
            if uid in uid_cache:
                user = uid_cache[uid]
            else:
                user = store.get_user(_id=sms.user_id)
                if not user:
                    logger.error("Cannot find user_id %d, skipping." % uid)
                    continue
                uid_cache[uid] = user

            logger.debug("Sending SMS with API id '%s...'" % user.api_id[4:])
            ret = send_sms(sms.text, user.api_id, user.api_key)
            logger.debug("return %s" % str(ret))
            logger.debug("deleting SMS")
            store.del_sms(sms)
            sleep(0.2) # this gives us a maximum of 5*60=300 SMSes/second

        logger.debug('Going to sleep.')
        sleep(60)

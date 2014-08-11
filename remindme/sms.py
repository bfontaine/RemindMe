# -*- coding: UTF-8 -*-

import pytz
from datetime import datetime, date, time

from log import logger
from store import SMS

from providers.base import MissingConfigParameter, ServerError, SMSException

# we only support 'Free' for now
from providers.free import FreeProvider as DefaultProvider

def send_sms(msg, api_id, api_key, **kw):
    """
    Send an SMS.
    """
    params = {'api_id': api_id, 'api_key': api_key}

    return DefaultProvider(params).send(msg)


def schedule_sms(msg, when, user_id):
    """
    Schedule an SMS to be sent later. If ``when`` is earlier than today the SMS
    is discarded. Return a boolean.
    """
    now = datetime.combine(date.today(), time()).replace(tzinfo=pytz.UTC)

    if when < now:
        logger.warn("%s is earlier than today. Discarding." % str(when))
        return False

    params = {
        'user_id': user_id,
        'text': msg,
        'send_on': when
    }

    s = SMS(params)
    s.save()
    logger.debug("Saving SMS %s to be sent on %s" % (str(s), str(when)))
    return True


if False:  # silent pyflakes
    MissingConfigParameter, ServerError, SMSException

# -*- coding: UTF-8 -*-

import pytz
from datetime import datetime

from log import logger
from store import SMS

from providers.base import MissingConfigParameter, ServerError, SMSException

# we only support 'Free' for now
from providers.free import FreeProvider as DefaultProvider

def utcnow():
    """
    Return a timezone-aware UTC datetime for the current time.
    """
    return datetime.utcnow().replace(tzinfo=pytz.utc)


def to_utc(d):
    return d.astimezone(pytz.utc)


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

    when = to_utc(when)

    if when < utcnow():
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

# -*- coding: UTF-8 -*-

import pytz
from datetime import datetime, date, time

from log import logger
from store import SMS

from providers.base import MissingConfigParameter, ServerError, SMSException

# we only support 'Free' for now
from providers.free import FreeProvider as DefaultProvider

# TODO improve this API, 'user' & 'pass' should be 'id' and 'key'

def send_sms(msg, params):
    """
    Send an SMS. ``params`` should have the following keys: ``user``, ``pass``.
    """
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

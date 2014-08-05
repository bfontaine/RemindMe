# -*- coding: UTF-8 -*-

import logging
import pytz
from datetime import datetime, date, time
from dateutil.parser import parse as parse_date

from store import SMS

from providers.base import MissingConfigParameter, ServerError, SMSException

# we only support 'Free' for now
from providers.free import FreeProvider as DefaultProvider

logger = logging.getLogger('rm.sms')
logger.addHandler(logging.StreamHandler())


def send_sms(msg, params):
    """
    Send an SMS. ``params`` should have the following keys: ``user``, ``pass``.
    """
    return DefaultProvider(params).send(msg)


def schedule_sms(msg, when, params):
    """
    Schedule an SMS to be sent later. If ``when`` is earlier than today the SMS
    is discarded. Return ``True`` or ``False``.
    """
    try:
        when = parse_date(when)
    except Exception as e:
        logger.error(e)
        return False

    now = datetime.combine(date.today(), time()).replace(tzinfo=pytz.UTC)

    if when < now:
        logger.warn("%s is earlier than today. Discarding." % str(when))
        return False

    params['text'] = msg
    params['send_on'] = when
    s = SMS(params)
    s.save()
    logger.debug("Saving SMS %s to be sent on %s" % (str(s), str(when)))
    return True


if False:  # silent pyflakes
    MissingConfigParameter, ServerError, SMSException

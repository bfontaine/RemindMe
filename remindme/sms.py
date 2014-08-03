# -*- coding: UTF-8 -*-

import logging

from providers.base import MissingConfigParameter, ServerError, SMSException

# we only support 'Free' for now
from providers.free import FreeProvider as DefaultProvider

logger = logging.getLogger('rm.sms')


def send_sms(msg, when, params):
    """
    Send an SMS. ``params`` should have the following keys: ``user``, ``pass``.
    """
    logger.warn("Sending the SMS right now. 'when' is unsupported.")
    return DefaultProvider(params).send(msg)


if False:  # silent pyflakes
    MissingConfigParameter, ServerError, SMSException

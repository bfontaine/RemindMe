# -*- coding: UTF-8 -*-

# we only support 'Free' for now
from providers.free import FreeProvider as DefaultProvider


def send_sms(msg, params):
    """
    Send an SMS. ``params`` should have the following keys: ``user``, ``pass``.
    """
    return DefaultProvider(params).send(msg)

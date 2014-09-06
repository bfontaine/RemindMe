# -*- coding: UTF-8 -*-

import json as _json
from dateutil.parser import parse as parse_date
from flask import Response

from log import logger
from core import schedule_sms
from flaskutils import user


def wrap_json(what, code=200):
    return Response(_json.dumps(what), code, mimetype='application/json')


def json(route):
    """
    Decorator. JSON-ify what is returned by a route and wraps it into a proper
    flask ``Response``, as well as make the function take a JSON payload and
    transform it into a dict.
    """
    def _route(payload):
        data = _json.loads(payload)
        what = route(data)
        return wrap_json(what)
    _route.__name__ = route.__name__
    return _route


@json
def api_schedule_sms(data):
    text, when = data['text'], data['when']

    try:
        when = parse_date(when)
    except Exception as e:
        logger.error(e)
        return {'status': False}

    ret = schedule_sms(text, when, user()._id)

    return {'status': ret}

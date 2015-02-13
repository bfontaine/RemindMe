# -*- coding: UTF-8 -*-


from freesms import FreeClient
from base import BaseProvider, MissingConfigParameter, ServerError


class FreeProvider(BaseProvider):
    """
    This is a provider class for the French telco 'Free'.

    >>> f = FreeProvider({'api_id': '12345678', 'api_key':'xyz'})
    >>> f.send('Hello, World!')
    True
    """

    def required_keys(self):
        return ['api_id', 'api_key']

    def send(self, msg):
        params = {
            'user': self.params['api_id'],
            'passwd': self.params['api_key']
        }
        f = FreeClient(**params)
        res = f.send_sms(msg)

        if res.status_code == 200:
            return True
        if res.status_code == 400:
            raise MissingConfigParameter()
        if res.status_code == 500:
            raise ServerError()
        return False

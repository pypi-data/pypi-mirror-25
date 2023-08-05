import time
import uuid
import logging

from jose import jws
from ambisafe_tenant.crypt import HMAC

logger = logging.getLogger('ambisafe_tenant')


class SecondFactorAuth(object):
    def __init__(self, api_key, key_secret, data, uri):
        self.api_key = api_key
        self.key_secret = key_secret
        self.uri = uri
        self.data = data

    def __call__(self, request):
        """
        :param request:
        :type request: requests.PreparedRequest
        :return:
        """
        hmac = HMAC(self.api_key, self.key_secret, self.uri, self.data)
        request.headers['API-NONCE'] = hmac.nonce
        request.headers['API-SIGNATURE'] = hmac.signature
        request.headers['API-KEY'] = self.api_key
        logger.debug('Secondfactor request is: {}'.format(request))
        logger.debug('Secondfactor nonce is: {}'.format(request.headers['API-NONCE']))
        return request


class AmbisafeTenantAuth(object):
    def __init__(self, api_key, api_secret, resource):
        self.api_key = api_key
        self.api_secret = api_secret
        self.resource = resource

    def __call__(self):
        return self.get_jws_token()

    def get_jws_token(self):
        payload = {
            "iss": self.api_key,
            "jti": str(uuid.uuid4()),
            "sub": self.resource,
            "aud": 'ambisafe',
            "exp": int(time.time()) + (60 * 60)
        }
        signed = jws.sign(payload, self.api_secret)
        return signed
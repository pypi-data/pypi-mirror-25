import base64
import hashlib
import hmac
import time

import requests
from requests.auth import AuthBase


class ArmAuth(AuthBase):
    def __init__(self, api_key):
        self.api_key = api_key

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        message = message.encode('ascii')
        hmac_key = base64.b64decode(self.api_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest())
        request.headers.update({
            'Content-Type': 'Application/JSON',
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'Authorization': 'Token {}'.format(self.api_key)
        })
        return request


class AuthenticatedClient:
    def __init__(self, api_key, api_url):
        self.url = api_url.strip('/')
        self.auth = ArmAuth(api_key)

    def get_variation(self, experiment, timeout=30):
        r = requests.get(self.url + '/{}/draw/'.format(experiment), auth=self.auth, timeout=timeout)
        print(r)
        return r.json()

    def reward(self, experiment, variation, timeout=30):
        r = requests.get(self.url + '/{}/{}/reward/'.format(experiment, variation), auth=self.auth, timeout=timeout)
        print(r)
        return r.json()

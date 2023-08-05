# coding: utf-8
import requests
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey.RSA import construct

from ._compat import urlencode


CAPITALIST_API_ENDPOINT = 'https://api.capitalist.net/'


class CapitalistClient(object):

    def __init__(self, username, password, root_url=CAPITALIST_API_ENDPOINT, max_retries=0):
        self.username = username
        self.password = password
        self.root_url = root_url
        self.max_retries = max_retries

    @property
    def session(self):
        if not hasattr(self, '_session'):
            self._session = requests.Session()
            adapter = requests.adapters.HTTPAdapter(max_retries=self.max_retries)
            self._session.mount('http://', adapter)
            self._session.mount('https://', adapter)
        return self._session

    def _call(self, operation, **kwargs):
        kwargs.update({'login': self.username, 'operation': operation})
        data = urlencode(kwargs)
        response = self.session.post(
            self.root_url,
            data=data,
            headers={'x-response-format': 'json', 'Content-Type': 'application/x-www-form-urlencoded'}
        )
        return response.json()

    def _secure_call(self, *args, **kwargs):
        # TODO. Get new token on code 20.
        if not hasattr(self, 'token'):
            self.setup_secure_session()
        return self._call(*args, token=self.token, encrypted_password=self.encrypted_password, **kwargs)

    def setup_secure_session(self):
        response = self.get_token()
        self.encrypted_password = EncryptedPassword(
            self.password,
            response['data']['modulus'],
            response['data']['exponent']
        )
        self.token = response['data']['token']

    def get_token(self):
        return self._call('get_token')

    def currency_rates(self):
        return self._secure_call('currency_rates')


class EncryptedPassword(object):
    """
    PKCS1 v1.5 encrypted password.
    """

    def __init__(self, password, modulus, exponent):
        self.password = password.encode()
        modulus = int(modulus, 16)
        exponent = int(exponent, 16)
        rsa = construct((modulus, exponent))
        self.cipher = PKCS1_v1_5.new(rsa)

    def __str__(self):
        return self.cipher.encrypt(self.password).hex()

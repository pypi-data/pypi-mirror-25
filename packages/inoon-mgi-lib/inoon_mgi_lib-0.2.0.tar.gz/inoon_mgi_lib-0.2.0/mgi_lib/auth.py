# -*- coding: utf-8 -*-
import json

import requests

from mgi_lib.errs import WrongCredentialException


class Credential():
    def __init__(self, jwt, expire_ms):
        self._jwt = jwt
        self._expire_ms = expire_ms

    @property
    def jwt(self):
        return self._jwt


class Auth():
    @classmethod
    def login(cls, username, password):
        resp = requests.post(url='https://auth.ino-on.com/auth/',
                             json={'username': username, 'password': password})

        if resp.status_code != requests.codes.ok:
            raise WrongCredentialException

        try:
            token_resp = json.loads(resp.content.decode())
            return Credential(jwt=token_resp['token'],
                              expire_ms=token_resp['expire_ms'])
        except:
            raise WrongCredentialException

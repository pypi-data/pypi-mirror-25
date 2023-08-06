# -*- encoding: utf-8 -*-
import json

import requests

from mgi_lib.api import MGIRequest
from mgi_lib import errs


class DeactiveDevice():
    base = 'https://themingam.ino-on.com/api/device/deactive/'
    ver = 'v2'

    @classmethod
    def list(cls, credential):
        if credential is None:
            raise errs.WrongCredentialException

        code, content = MGIRequest.get(url=cls.base,
                                       jwt=credential.jwt,
                                       ver=cls.ver)

        if code == requests.codes.forbidden:
            raise errs.WrongCredentialException

        return json.loads(content)

    @classmethod
    def get(cls, credential, ltid):
        if credential is None:
            raise errs.WrongCredentialException

        url = '{}{}/'.format(cls.base, ltid)
        code, content = MGIRequest.get(url=url,
                                       jwt=credential.jwt,
                                       ver=cls.ver)

        if code == requests.codes.forbidden:
            raise errs.WrongCredentialException

        if code == requests.codes.not_found:
            raise errs.NonExistException

        return json.loads(content)


class ActiveDevice():
    base = 'https://themingam.ino-on.com/api/device/active/'
    ver = 'v2'

    @classmethod
    def list(cls, credential):
        if credential is None:
            raise errs.WrongCredentialException

        code, content = MGIRequest.get(url=cls.base,
                                       jwt=credential.jwt,
                                       ver=cls.ver)

        if code == requests.codes.forbidden:
            raise errs.WrongCredentialException

        return json.loads(content)

    @classmethod
    def get(cls, credential, ltid):
        if credential is None:
            raise errs.WrongCredentialException

        url = '{}{}/'.format(cls.base, ltid)
        code, content = MGIRequest.get(url=url,
                                       jwt=credential.jwt,
                                       ver=cls.ver)

        if code == requests.codes.forbidden:
            raise errs.WrongCredentialException

        if code == requests.codes.not_found:
            raise errs.NonExistException

        return json.loads(content)

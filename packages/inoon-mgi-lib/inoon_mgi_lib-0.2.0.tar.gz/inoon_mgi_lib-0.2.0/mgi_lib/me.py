import json

import requests

from mgi_lib.api import MGIRequest
from mgi_lib import errs


class Me():
    base = 'https://themingam.ino-on.com/api/me/'
    ver = 'v1'

    @classmethod
    def me(cls, credential):
        if credential is None:
            raise errs.WrongCredentialException

        code, content = MGIRequest.get(url=cls.base,
                                       jwt=credential.jwt,
                                       ver=cls.ver)

        if code == requests.codes.unauthorized:
            raise errs.WrongCredentialException

        return json.loads(content)

import abc

import requests


class MGIRequest():
    @classmethod
    def get(cls, url, jwt, ver):
        resp = requests.get(url=url, headers={
            'Accept': 'application/json; version={}'.format(ver),
            'Authorization': 'jwt {}'.format(jwt)
        })

        return resp.status_code, resp.content.decode()


class MGIApi(abc.ABC):
    @abc.abstractmethod
    def version(self):
        pass

    @abc.abstractmethod
    def url(self):
        pass

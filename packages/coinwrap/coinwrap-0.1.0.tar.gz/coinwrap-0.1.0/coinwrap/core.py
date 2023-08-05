import requests


class Market(object):  # A.1

    _session = None  # A.2

    def __init__(self, url='https://api.coinmarketcap.com/v1/', timeout=120):  # A.3
        self.url = url
        self.timeout = timeout

    @property  # A.8
    def session(self):  # A.4
        self._session = requests.Session()
        self._session.headers.update({'Content-Type': 'application/json'})
        self._session.headers.update({'User-agent': 'github:bitforce/wrapper-py-coinmarketcap'})
        return self._session

    def __request(self, endpoint, params):  # A.5
        response_object = self.session.get(self.url + endpoint, params=params, timeout=self.timeout)
        return response_object.json()

    def coin(self, currency='', **kwargs):  # A.6
            return self.__request('ticker/' + currency, {}.update(kwargs))

    def stats(self, **kwargs):  # A.7
            return self.__request('global/', {}.update(kwargs))

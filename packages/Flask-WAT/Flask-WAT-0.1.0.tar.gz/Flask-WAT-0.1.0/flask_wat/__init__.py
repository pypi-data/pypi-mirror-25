# -*- coding: utf-8 -*-
import requests


class Wat(object):

    def __init__(self, server_url, app=None):
        self.server_url = server_url
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        username = app.config['WAT_USERNAME']
        password = app.config['WAT_PASSWORD']
        verify = app.config.get('WAT_VERIFY')

        self.wat_session = requests.Session()
        self.wat_session.auth = (username, password)
        self.wat_session.verify = verify

        self.session = requests.Session()

    def get_access_token(self):
        r = self.wat_session.get(self.server_url)
        return r.json()['access_token']

    def request(self, method, url, params={}, **kwargs):
        params['access_token'] = self.get_access_token()
        return self.session.request(method=method, url=url,
                                    params=params, **kwargs)

    def get(self, url, params={}, **kwargs):
        kwargs.setdefault('allow_redirects', True)
        return self.request('get', url, params=params, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.session.request('post', url, data=data, json=json,
                                    **kwargs)

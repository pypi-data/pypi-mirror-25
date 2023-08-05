# coding=utf-8

from urlparse import parse_qs, parse_qsl

class Request(object):

    def __init__(self, env):
        self._env = env
        self._parse_env(env)
        self._translator = lambda x: x

    def _parse_env(self, env):
        self._path = env['PATH_INFO']
        self._query = parse_qsl(env['QUERY_STRING'])
        self._content_length = int(env.get('CONTENT_LENGTH', '0'))
        self._request_method = env['REQUEST_METHOD'].lower()

        self._post_data = {}
        if self.is_post() and self.get_content_length() > 0:
            self._raw_post = env['wsgi.input'].read()
            self._post_data = dict(parse_qsl(self._raw_post))

        self._custom_data = {}

    def is_get(self):
        return self._request_method == 'get'

    def is_post(self):
        return self._request_method == 'post'

    def get_content_length(self):
        return self._content_length

    def get_raw_post(self):
        return self._raw_post

    def get_post_data(self):
        return self._post_data

    def get_query_data(self):
        return self._query

    def get_path(self):
        return self._path

    def get_header(self, name):
        header = 'HTTP_{}'.format(name.upper().replace('-','_'))
        return self._env.get(header)

    def set_custom(self, name, value):
        self._custom_data[name] = value

    def set_translator(self, t):
        self._translator = t

    def get(self, name, default=None):
        return self[name] or default

    def _(self, msg):
        return self._translator(msg)

    def __getitem__(self, item):
        if item in self._custom_data:
            return self._custom_data[item]

        if self.is_post() and item in self._post_data:
            return self._post_data[item]

        return self._query.get(item)

# coding=utf-8

class Response(object):
    def __init__(self, content=''):
        self._status = '200 OK'
        self._content_type = 'text/plain'
        self._content = content

    def get_status(self):
        return self._status

    def get_headers(self):
        return [('Content-type', self._content_type)]

    def get_content(self):
        return self._content

class JsonResponse(Response):
    def __init__(self, content):
        super(JsonResponse, self).__init__(content)
        self._content_type = 'application/json'
        self._content = content

    def get_content(self):
        import json
        return json.dumps({
            'ok': self.get_status() == '200 OK',
            'content': self._content or {}
        })

class JsonNotFoundResponse(JsonResponse):
    def __init__(self, content=None):
        super(JsonNotFoundResponse, self).__init__(content)
        self._status = '404 Not Found'


class JsonBadRequest(JsonResponse):
    def __init__(self, field, error, message):
        content = dict(error=u"{}_{}".format(field, error), message=message)
        super(JsonBadRequest, self).__init__(content)
        self._status = '400 Bad Request'


class JsonUnauthorizedResponse(JsonResponse):
    def __init__(self, content=None):
        super(JsonUnauthorizedResponse, self).__init__(content)
        self._status = '401 Unauthorized'

class JsonServerError(JsonResponse):
    def __init__(self, content=None):
        super(JsonUnauthorizedResponse, self).__init__(content)
        self._status = '500 Server Error'

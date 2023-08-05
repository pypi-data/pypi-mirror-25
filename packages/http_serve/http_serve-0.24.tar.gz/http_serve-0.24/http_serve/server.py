# coding=utf-8

from gevent.pywsgi import WSGIServer

from .errors import ErrorResponse
from .request import Request
from .response import JsonServerError

class HttpServer(object):
    def __init__(self, host, port, log, router, request_cls=None):
        """
        @type host: str
        @type port: int
        @type log: logging.Logger
        @type router: http_serve.router.Router
        @type request_cls:
        """
        self.__host = host
        self.__port = port
        self.__log = log
        self.__middleware = []
        self.__request_cls = request_cls or Request
        self.__router = router

    def add_middleware(self, middleware):
        """
        @type middleware: http_serve.middleware.Middleware
        @return:
        """
        self.__middleware.append(middleware)

    def handle_request(self, env, start_response):
        try:
            request = self.__request_cls(env)
            try:
                for middle in self.__middleware:
                    request = middle.pre_action(request)
                response = self.__router.run_action(request)
            except ErrorResponse as e:
                response = e.get_response()

            for middle in reversed(self.__middleware):
                response = middle.post_action(request, response)
        except Exception as e:
            self.__log.error(str(e))
            response = JsonServerError()

        start_response(response.get_status(), response.get_headers())
        return response.get_content()

    def serve_forever(self):
        ls = (self.__host, self.__port)
        self.__log.debug('Listening {}:{}'.format(*ls))
        WSGIServer(
            ls,
            self.handle_request,
            log=self.__log,
            error_log=self.__log
        ).serve_forever()



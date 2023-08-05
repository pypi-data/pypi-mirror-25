# coding=utf-8

from .errors import ErrorResponse
from .response import JsonNotFoundResponse

class Router(object):

    def __init__(self):
        self.__actions = {}

    def register_action(self, action_name, action):
        self.__actions[action_name] = action

    def run_action(self, request):
        """
        @type request: http_serve.request.Request
        @rtype: http_serve.response.Response
        """
        path = request.get_path().split('/')

        if path[0] == '':
            path = path[1:]
        action_name = '_'.join(path)
        if action_name not in self.__actions:
            raise ErrorResponse(JsonNotFoundResponse())

        return self.__actions[action_name](request)

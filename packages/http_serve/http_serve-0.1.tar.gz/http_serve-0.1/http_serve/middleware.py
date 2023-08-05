# coding=utf-8

import errors
from .response import JsonUnauthorizedResponse

class Middleware(object):

    def pre_action(self, request):
        """
        @type request: http_serve.request.Request
        @rtype: http_serve.request.Request
        """
        return request

    def post_action(self, request, response):
        """
        @type request: http_serve.request.Request
        @type response: http_serve.response.Response
        @rtype: http_serve.response.Response
        """
        return response


class Authorization(Middleware):

    def __init__(self, token_to_user):
        self.__token_to_user = token_to_user

    def pre_action(self, request):
        """
        @type request: wizdom.shared.lib.http_serve.request.Request
        @rtype: wizdom.shared.lib.http_serve.request.Request
        """
        token = request.get_header('X-AUTH-TOKEN')
        if not token:
            request.set_custom('is_authorized', False)
            return request

        try:
            user = self.__token_to_user(token)
            request.set_custom('is_authorized', True)
            request.set_custom('user', user)
        except:
            request.set_custom('user', None)
            request.set_custom('is_authorized', False)
        return request

class Localization(Middleware):

    def __init__(self, user_to_translator):
        self.__user_to_translator = user_to_translator

    def pre_action(self, request):
        """
        @type request: wizdom.shared.lib.http_serve.request.Request
        @rtype: wizdom.shared.lib.http_serve.request.Request
        """
        if request['is_authorized']:
           request.set_translator(self.__user_to_translator(request['user']))

        return request


class AuthorizationRequired(Middleware):

    def pre_action(self, request):
        """
        @type request: wizdom.shared.lib.http_serve.request.Request
        @rtype: wizdom.shared.lib.http_serve.request.Request
        """
        if not request['is_authorized']:
            raise errors.ErrorResponse(JsonUnauthorizedResponse())
        return request

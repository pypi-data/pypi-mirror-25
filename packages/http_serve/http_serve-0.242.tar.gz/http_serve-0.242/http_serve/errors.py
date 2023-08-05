# coding=utf-8

class ErrorResponse(Exception):
    def __init__(self, response):
        self.__response = response

    def get_response(self):
        return self.__response

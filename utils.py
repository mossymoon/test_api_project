from datetime import datetime

import logging

# import curlify
import requests


logger = logging.getLogger(__name__)


def log_request_response(response):
    logger.debug(f"Request URL: {response.request.url}")
    logger.debug(f"Request Method: {response.request.method}")
    logger.debug(f"Request Headers: {response.request.headers}")
    logger.debug(f"Request Body: {response.request.body}")
    logger.debug(f"Response Status Code: {response.status_code}")
    logger.debug(f"Response Headers: {response.headers}")
    logger.debug(f"Response Body: {response.text}")


def get(url, **kwargs):
    response = requests.get(url, **kwargs)
    log_request_response(response)
    return response


def post(url, data=None, json=None, **kwargs):
    response = requests.post(url, data=data, json=json, **kwargs)
    log_request_response(response)
    return response



class Objects:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        for item in args:
            setattr(self, item, None)

    def as_dict(self) -> dict:
        return self.__dict__

    def add_attribute(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        for item in args:
            setattr(self, item, None)

    def del_attribute(self, *args: str):
        for item in args:
            self.__delattr__(item)

    def from_dict(self, data: dict):
        for k, v in data.items():
            setattr(self, k, v)

    def as_dict_custom(self, *args: str) -> dict:
        data = self.as_dict()
        not_need = set(data) - set(args)
        for item in not_need:
            data.pop(item)
        return data

    def get_attributes(self) -> set:
        return set(self.as_dict())

def timestamp():
    return str(int(datetime.now().timestamp()))

# def get_curl(response):
#     return curlify.to_curl(response.request)


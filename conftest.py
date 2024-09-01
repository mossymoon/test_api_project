import requests
import pytest
from utils import post

url_post = "https://api.restful-api.dev/objects"
url_put = "https://api.restful-api.dev/objects"
url_get = "https://api.restful-api.dev/objects"



@pytest.fixture()
def post_method(data_for_json):
    response = post(url=url_post, json=data_for_json)

    return response


@pytest.fixture()
def put_method(data_for_json, id, color):
    data = data_for_json
    data['data'].update({"color": color})
    req = requests.put(url=f"{url_put}/{id}", json=data)
    return req


@pytest.fixture()
def patch_method(name, id):
    data = {"name": name}
    req = requests.patch(url=f"{url_put}/{id}", json=data)
    return req


@pytest.fixture()
def get_method():
    response = requests.get(url=url_get)
    return response


@pytest.fixture()
def get_method_id(id):
    params = {"id": id}
    response = requests.get(url=url_get, params=params)
    return response

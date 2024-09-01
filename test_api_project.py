import requests
import re
from pytest import fixture, mark

url = "https://api.restful-api.dev/objects"



@fixture()
def data_for_json(computer_name, year, price, model, memory):
    json = {
        "name": computer_name,
        "data": {
          "year": year,
          "price": price,
          "CPU model": model,
          "Hard disk size": memory
       }
    }
    return json


class TestPost:
    @mark.parametrize("computer_name, year, price, model, memory",
                      [("Apple MacBook Pro 16", 2020, 1849.99, "Intel Core i9", "1 TB"),
                       ("Apple MacBook Pro 56", 2023, 1849.99, "Intel Core i9", "1 TB")])
    def test_post(self, post_method, computer_name, year, price, model, memory):
        response = post_method
        assert response.status_code == 200
        assert response.content != {}
        assert True
        print(response.json())

    @mark.parametrize("computer_name, year, price, model, memory",
                      [("Apple MacBook Pro 16", 2020, 1849.99, "Intel Core i9", "1 TB")])
    def test_post_response(self, post_method, computer_name, year, price, model, memory):
        response = post_method
        assert response.json()["id"] != ""
        assert response.json()["name"] == "Apple MacBook Pro 16"
        timestamp = response.json()["createdAt"]
        pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}\+\d{2}:\d{2}$"
        match = re.match(pattern, timestamp)
        assert timestamp == match.group()

    @mark.parametrize("computer_name, year, price, model, memory",
                      [("Apple MacBook Pro 16", 2020, 1849.99, "Intel Core i9", "1 TB ")])
    def test_post_response_inv(self, post_method, data_for_json, computer_name, year, price, model, memory):
        json_data = data_for_json
        json_data.pop("name")
        json_data.pop("data")

        response = requests.post(url=url, json=data_for_json)

        assert response.status_code == 200
        assert response.json()["createdAt"] != ""
        assert response.json()["id"] != ""
        assert response.json()["name"] is None
        assert response.json()["data"] is None
        print(response.json())


class TestPut:
    @mark.parametrize("computer_name, year, price, model, memory, id",
                      [(
                              "Apple MacBook Pro 16", 2020, 1849.99, "Intel Core i9", "1 TB",
                              "ff80818191aa69a90191ac30a7210220"
                      )])
    @mark.parametrize("color", ["blue", "green", "red", "pink"])
    def test_put_color(self, put_method, computer_name, year, price, model, memory, color, id):
        response = put_method
        assert response.status_code == 200
        assert response.content != {}
        assert response.json()["data"]["color"] == color

    @mark.parametrize("computer_name, year, price, model, memory, color",
                      [(
                              "Apple MacBook Pro 16", 2020, 1849.99, "Intel Core i9", "1 TB", "green"
                      )])
    @mark.parametrize("id", [3, 5, 7, 8, 10, 4])
    def test_put_neg(self, put_method, computer_name, year, price, model, memory, id):
        response = put_method
        assert response.status_code == 405
        assert response.content != {}
        assert response.json()["error"] == (f'{id} is a reserved id and the data object of it cannot be overridden. You can create a new object '
                                            'via POST request and use new generated by id from it to send a PUT request.')


class TestPatch:
    @mark.parametrize("name",
                      ["Apple MacBook Pro 787896", "Apple is not apple"])
    @mark.parametrize("id", ["ff80818191ad7c2f0191ade5be4b00b8"])
    def test_patch(self, patch_method, name, id):
        response = patch_method
        # print(utils.get_curl(response))
        print(response.json())
        assert response.status_code == 200
        assert response.json()["name"] == name
        assert response.content != {}


class TestGet:
    def test_get_all(self, get_method):
        response = get_method
        print(response.json())

    @mark.parametrize("id", [5, 6, 2, 1, 5, 4, 7])
    def test_get_all_id(self, get_method_id, id):
        data = get_method_id
        data.params = {"id": id}
        assert data.json()[0]["id"] == str(id)

    @mark.parametrize("id", ["$£@!%$", "*&*^))(("])
    def test_get_all_id_inv(self, get_method_id, id):
        params = {"id": id}
        response = requests.get(url=url, params=params)
        assert response.status_code == 200
        assert response.json() == []

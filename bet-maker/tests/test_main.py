from collections import namedtuple

import allure
import pytest as pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

# In this file I leave basic examples of tests. Please make sure tests are written for all endpoints.


def test_root():
    with allure.step("API root message"):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "BetAPI is running"}


NameParams = namedtuple('NameParams', ['return_code', 'name', 'response_dict'])


@pytest.fixture(scope="function", params=[NameParams(404, 'bad_endpoint', {'detail': 'Not Found'}),
                                          NameParams(404, 'bad_endpoint1', {'detail': 'Not Found'})],
                ids=['Param example name 1', 'Param example name 2'])
def name_data(request):
    return request.param


@allure.step("Params example")
def test_root_hello_name(name_data: NameParams):
    with allure.step(f"API call with param {name_data}"):
        response = client.get(f"/{name_data}")
        assert response.status_code == name_data.return_code
        assert response.json() == name_data.response_dict

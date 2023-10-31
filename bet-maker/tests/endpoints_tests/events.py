import allure

from app.adapters.shemas import Event, EventState
from tests.endpoints_tests import test_client


@allure.step("Positive test of get event endpoint")
def test_get_events():
    result = test_client.get('/events')
    with allure.step("Response code is 200"):
        assert result.status_code == 200
    with allure.step("Response is not empty"):
        assert result.json() != []
    with allure.step("Response contains valid events"):
        events = [Event.model_validate(event) for event in result.json()]
    with allure.step("Only new events are returned"):
        assert all(event.state == EventState.NEW for event in events)

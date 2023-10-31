import allure

from app.adapters.shemas import Bet
from tests.endpoints_tests import test_client


@allure.step("Positive test of get bets endpoint")
def test_get_bets():
    result = test_client.get('/bets')
    with allure.step("Response code is 200"):
        assert result.status_code == 200
    with allure.step("Response contains valid bets"):
        assert [Bet.model_validate(bet) for bet in result.json()]

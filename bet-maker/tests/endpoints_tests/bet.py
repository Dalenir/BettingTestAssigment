import allure

from app.adapters.shemas import BetBasic, EventState
from app.api.endpoints.bet.bet_on_event import NewBetResponse
from tests.endpoints_tests import test_client


@allure.step("Positive test of bet on valid event")
def test_bet_on_valid_event():

    bet = BetBasic(
        event_id="145",
        bet_amount=100,
        bet_on_event_state=EventState("Win")
    )

    result = test_client.put('/bet', json=bet.model_dump(mode='json'))

    with allure.step("Response code is 200"):
        assert result.status_code == 200
    with allure.step("Returned valid responce"):
        new_bet = NewBetResponse.model_validate(result.json())
    with allure.step("Bet is correct"):
        assert new_bet.event_id == bet.event_id
        assert new_bet.bet_amount == bet.bet_amount
        assert new_bet.bet_on_event_state == bet.bet_on_event_state
        assert new_bet.id is not None
    with allure.step("Potential win amount is correct"):
        print(new_bet.payment_on_win, bet.bet_amount * new_bet.event.coefficient)
        assert new_bet.payment_on_win == bet.bet_amount * new_bet.event.coefficient

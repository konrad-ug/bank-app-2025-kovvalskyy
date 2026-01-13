import pytest
from src.account import Account
from src.business_account import BusinessAccount


@pytest.fixture()
def personal():
    return Account("John", "Doe", "12345678901")


@pytest.fixture()
def business(mocker):
    mocker.patch(
        "src.business_account.BusinessAccount.is_nip_active_in_mf",
        return_value=True,
    )
    return BusinessAccount(company_name="Acme", nip="1234567890")


class TestExpressTransfers:

    @pytest.mark.parametrize(
        "start_balance, amount, expected_ok, expected_balance",
        [
            (100.0, 100.0, True, -1.0),
            (99.0, 100.0, False, 99.0),
        ],
    )
    def test_express_out_personal(
        self, personal, start_balance, amount, expected_ok, expected_balance
    ):
        personal.transfer_in(start_balance)
        ok = personal.express_out(amount)
        assert ok is expected_ok
        assert personal.balance == expected_balance

    @pytest.mark.parametrize(
        "start_balance, amount, expected_ok, expected_balance",
        [
            (100.0, 100.0, True, -5.0),
            (50.0, 60.0, False, 50.0),
        ],
    )
    def test_express_out_business(
        self, business, start_balance, amount, expected_ok, expected_balance
    ):
        business.transfer_in(start_balance)
        ok = business.express_out(amount)
        assert ok is expected_ok
        assert business.balance == expected_balance

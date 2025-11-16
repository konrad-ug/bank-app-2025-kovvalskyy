from src.account import Account
from src.business_account import BusinessAccount
import pytest


class TestTransfers:

    @pytest.fixture()
    def personal(self):
        return Account("John", "Doe", "12345678901")

    def test_incoming_transfer_increases_balance(self, personal):
        personal.transfer_in(200.0)
        assert personal.balance == 200.0

    @pytest.mark.parametrize(
        "deposit, withdraw, expected_ok, expected_balance",
        [
            (200.0, 150.0, True, 50.0),   # wystarczające srodki
            (100.0, 150.0, False, 100.0), # niewystarczające srodki
        ],
    )
    def test_outgoing_transfer_variants(
        self, personal, deposit, withdraw, expected_ok, expected_balance
    ):
        personal.transfer_in(deposit)
        ok = personal.transfer_out(withdraw)
        assert ok is expected_ok
        assert personal.balance == expected_balance

    def test_amount_must_be_positive(self, personal):
        assert personal.transfer_in(-10.0) is False
        assert personal.transfer_out(0.0) is False


class TestBusinessTransfers:

    @pytest.fixture()
    def business(self):
        return BusinessAccount("Acme Corp", "1234567890")

    def test_incoming_transfer_increases_balance(self, business):
        business.transfer_in(500.0)
        assert business.balance == 500.0

    @pytest.mark.parametrize(
        "deposit, withdraw, expected_ok, expected_balance",
        [
            (300.0, 200.0, True, 100.0),  # wystarczające środki
            (100.0, 150.0, False, 100.0), # niewystarczające srodki
        ],
    )
    def test_outgoing_transfer_variants(
        self, business, deposit, withdraw, expected_ok, expected_balance
    ):
        business.transfer_in(deposit)
        ok = business.transfer_out(withdraw)
        assert ok is expected_ok
        assert business.balance == expected_balance

    def test_amount_must_be_positive(self, business):
        assert business.transfer_in(-10.0) is False
        assert business.transfer_out(0.0) is False

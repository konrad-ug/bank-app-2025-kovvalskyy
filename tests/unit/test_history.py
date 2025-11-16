import pytest
from src.account import Account
from src.business_account import BusinessAccount


@pytest.fixture
def personal_account():
    return Account("John", "Doe", "12345678901")


@pytest.fixture
def business_account():
    return BusinessAccount("Acme", "1234567890")


class TestHistoryPersonal:
    def test_history_personal_in_out_express(self, personal_account):
        a = personal_account
        a.transfer_in(500.0)
        a.express_out(300.0)
        assert a.history == [500.0, -300.0, -1.0]

    def test_history_initially_empty_personal(self, personal_account):
        a = personal_account
        assert a.history == []

    def test_personal_history_not_changed_on_failed_transfer_out(self, personal_account):
        a = personal_account
        a.transfer_in(100.0)
        before = list(a.history)
        ok = a.transfer_out(150.0)
        assert ok is False
        assert a.history == before == [100.0]

    def test_personal_history_not_changed_on_failed_express_out(self, personal_account):
        a = personal_account
        a.transfer_in(50.0)
        before = list(a.history)
        ok = a.express_out(100.0)
        assert ok is False
        assert a.history == before == [50.0]

    def test_personal_negative_or_zero_amount_not_recorded(self, personal_account):
        a = personal_account
        a.transfer_in(-10.0)
        a.transfer_out(0.0)
        assert a.history == []

    def test_multiple_operations_order_personal(self, personal_account):
        a = personal_account
        a.transfer_in(100.0)
        a.transfer_in(50.0)
        a.transfer_out(30.0)
        a.express_out(20.0)  # -20, -1 fee
        assert a.history == [100.0, 50.0, -30.0, -20.0, -1.0]


class TestHistoryBusiness:
    def test_history_business(self, business_account):
        b = business_account
        b.transfer_in(200.0)
        b.transfer_out(50.0)
        b.express_out(100.0)
        assert b.history == [200.0, -50.0, -100.0, -5.0]

    def test_history_initially_empty_business(self, business_account):
        b = business_account
        assert b.history == []

    def test_business_history_not_changed_on_failed_transfer_out(self, business_account):
        b = business_account
        b.transfer_in(100.0)
        before = list(b.history)
        ok = b.transfer_out(150.0)
        assert ok is False
        assert b.history == before == [100.0]

    def test_business_history_not_changed_on_failed_express_out(self, business_account):
        b = business_account
        b.transfer_in(40.0)
        before = list(b.history)
        ok = b.express_out(50.0)
        assert ok is False
        assert b.history == before == [40.0]

    def test_business_negative_or_zero_amount_not_recorded(self, business_account):
        b = business_account
        b.transfer_in(-10.0)
        b.transfer_out(0.0)
        assert b.history == []

    def test_multiple_operations_order_business(self, business_account):
        b = business_account
        b.transfer_in(300.0)
        b.transfer_in(100.0)
        b.transfer_out(50.0)
        b.express_out(100.0)  # -100, -5 fee
        assert b.history == [300.0, 100.0, -50.0, -100.0, -5.0]

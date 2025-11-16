from src.account import Account
from src.business_account import BusinessAccount


class TestTransfers:
    def test_incoming_transfer_increases_balance(self):
        a = Account("John", "Doe", "12345678901")  # bez promo -> 0.0
        a.transfer_in(200.0)
        assert a.balance == 200.0

    def test_outgoing_transfer_requires_sufficient_funds(self):
        a = Account("John", "Doe", "12345678901")
        a.transfer_in(200.0)
        ok = a.transfer_out(150.0)
        assert ok is True
        assert a.balance == 50.0

    def test_outgoing_transfer_fails_when_insufficient(self):
        a = Account("John", "Doe", "12345678901")
        a.transfer_in(100.0)
        ok = a.transfer_out(150.0)
        assert ok is False
        assert a.balance == 100.0

    def test_amount_must_be_positive(self):
        a = Account("John", "Doe", "12345678901")
        assert a.transfer_in(-10.0) is False
        assert a.transfer_out(0.0) is False


class TestBusinessTransfers:
    def test_incoming_transfer_increases_balance(self):
        b = BusinessAccount("Acme Corp", "1234567890")
        b.transfer_in(500.0)
        assert b.balance == 500.0

    def test_outgoing_transfer_requires_sufficient_funds(self):
        b = BusinessAccount("Acme Corp", "1234567890")
        b.transfer_in(300.0)
        ok = b.transfer_out(200.0)
        assert ok is True
        assert b.balance == 100.0

    def test_outgoing_transfer_fails_when_insufficient(self):
        b = BusinessAccount("Acme Corp", "1234567890")
        b.transfer_in(100.0)
        ok = b.transfer_out(150.0)
        assert ok is False
        assert b.balance == 100.0

    def test_amount_must_be_positive(self):
        b = BusinessAccount("Acme Corp", "1234567890")
        assert b.transfer_in(-10.0) is False
        assert b.transfer_out(0.0) is False
from src.account import Account

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
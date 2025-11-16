from src.account import Account
from src.business_account import BusinessAccount

class TestExpressTransfers:
    def test_express_out_personal_allows_fee_overdraft(self):
        a = Account("John", "Doe", "12345678901")
        a.transfer_in(100.0)
        ok = a.express_out(100.0)  # fee 1 PLN
        assert ok is True
        assert a.balance == -1.0

    def test_express_out_personal_requires_amount_covered(self):
        a = Account("John", "Doe", "12345678901")
        a.transfer_in(99.0)
        ok = a.express_out(100.0)  # nie ma kwoty przelewu
        assert ok is False
        assert a.balance == 99.0

    def test_express_out_business_fee_5(self):
        b = BusinessAccount(company_name="Acme", nip="1234567890")
        b.transfer_in(100.0)
        ok = b.express_out(100.0)  # fee 5
        assert ok is True
        assert b.balance == -5.0

    def test_express_out_business_requires_amount_covered(self):
        b = BusinessAccount(company_name="Acme", nip="1234567890")
        b.transfer_in(50.0)
        ok = b.express_out(60.0)
        assert ok is False
        assert b.balance == 50.0
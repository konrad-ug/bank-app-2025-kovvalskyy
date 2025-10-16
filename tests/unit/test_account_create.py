from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678901")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "12345678901"

    def test_pesel_too_long(self):
        account = Account("Jane", "Doe", "123456789013e23")
        assert account.pesel == "Invalid"

    def test_pesel_none(self):
        account = Account("Jane", "Doe", None)
        assert account.pesel == "Invalid"

    def test_correct_promoCode(self):
        account = Account ("Alice", "Smith", "12345678901", "PROM_XYZ")
        assert account.balance == 50.0
    
    def test_promoCode_suffix_too_long(self):
        account = Account ("Alice", "Smith", "12345678901", "PROM_XYZZ")
        assert account.balance == 0.0

    def test_promoCode_suffix_too_short(self):
        account = Account ("Alice", "Smith", "12345678901", "PROM_XY")
        assert account.balance == 0.0

    def test_promoCode_wrong_suffix_minus(self):
        account = Account ("Alice", "Smith", "12345678901", "PROM-XYZ")
        assert account.balance == 0.0
import pytest
from src.account import Account


class TestAccount:

    @pytest.fixture()
    def names(self):
        return "John", "Doe"

    def test_account_creation(self, names):
        first, last = names
        account = Account(first, last, "12345678901")
        assert account.first_name == first
        assert account.last_name == last
        assert account.balance == 0.0
        assert account.pesel == "12345678901"

    @pytest.mark.parametrize(
        "pesel, expected",
        [
            ("123456789013e23", "Invalid"),
            (None, "Invalid"),
        ],
    )
    def test_pesel_invalid_variants(self, names, pesel, expected):
        first, last = names
        account = Account(first, last, pesel)
        assert account.pesel == expected

    @pytest.mark.parametrize(
        "pesel, promo, expected_balance",
        [
            ("12345678901", "PROM_XYZ", 50.0),     # poprawny kod
            ("12345678901", "PROM_XYZZ", 0.0),     # suffix za dlugi
            ("12345678901", "PROM_XY", 0.0),       # suffix za krotki
            ("12345678901", "PROM-XYZ", 0.0),      # zly separator
            ("59125678901", "PROM-XYZ", 0.0),      # za stary osoba + zlyy kod
            ("03305678901", "PROM_XYZ", 50.0),     # poprawna osoba + kod
        ],
    )
    def test_promoCode_variants(self, names, pesel, promo, expected_balance):
        first, last = names
        account = Account(first, last, pesel, promo)
        assert account.balance == expected_balance
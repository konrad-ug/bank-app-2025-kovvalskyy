from src.account import BusinessAccount

class TestBusinessAccount:
    def test_business_account_fields_and_no_promo(self):
        b = BusinessAccount(company_name="Acme Sp. z o.o.", nip="1234567890", promoCode="PROM_XYZ")
        assert b.company_name == "Acme Sp. z o.o."
        assert b.nip == "1234567890"
        assert b.balance == 0.0  # brak promocji dla kont firmowych

    def test_business_account_invalid_nip(self):
        b = BusinessAccount(company_name="Foo", nip="12345")
        assert b.nip == "Invalid"

    def test_business_account_transfers(self):
        b = BusinessAccount(company_name="Acme", nip="1234567890")
        b.transfer_in(500.0)
        assert b.balance == 500.0
        assert b.transfer_out(200.0) is True
        assert b.balance == 300.0
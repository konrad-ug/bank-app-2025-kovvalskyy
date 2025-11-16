from src.business_account import BusinessAccount

class TestBusinessAccount:
    def test_business_account_invalid_nip(self):
        b = BusinessAccount(company_name="Foo", nip="12345")
        assert b.nip == "Invalid"
        
    def test_business_account_valid_nip(self):
        b = BusinessAccount(company_name="Bar", nip="1234567890")
        assert b.nip == "1234567890"
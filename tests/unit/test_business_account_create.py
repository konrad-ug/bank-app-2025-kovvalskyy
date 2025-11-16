import pytest
from src.business_account import BusinessAccount


class TestBusinessAccount:

    @pytest.mark.parametrize(
        "nip, expected",
        [
            ("12345", "Invalid"),
            ("1234567890", "1234567890"),
        ],
    )
    def test_business_account_nip_variants(self, nip, expected):
        b = BusinessAccount(company_name="FooBar", nip=nip)
        assert b.nip == expected

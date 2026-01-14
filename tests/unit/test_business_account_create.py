import pytest
from src.business_account import BusinessAccount


class TestBusinessAccount:

    @pytest.mark.parametrize(
        "nip, expected",
        [
            ("12345", "12345"),
            ("1234567890", "1234567890"),
        ],
    )
    def test_business_account_nip_variants(self, mocker, nip, expected):
        if isinstance(nip, str) and len(nip) == 10 and nip.isdigit():
            mocker.patch(
                "src.business_account.BusinessAccount.is_nip_active_in_mf",
                return_value=True,
            )
        b = BusinessAccount(company_name="FooBar", nip=nip)
        assert b.nip == expected

    def test_constructor_raises_when_company_not_registered(self, mocker):
        mocker.patch(
            "src.business_account.BusinessAccount.is_nip_active_in_mf",
            return_value=False,
        )

        with pytest.raises(ValueError) as err:
            BusinessAccount(company_name="FooBar", nip="1234567890")

        assert str(err.value) == "Company not registered!!"
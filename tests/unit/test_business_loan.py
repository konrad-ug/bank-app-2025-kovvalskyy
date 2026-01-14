import pytest
from src.business_account import BusinessAccount


class TestBusinessLoan:

    @pytest.fixture()
    def account(self, mocker):
        mocker.patch(
            "src.business_account.BusinessAccount.is_nip_active_in_mf",
            return_value=True,
        )
        return BusinessAccount("Acme", "1234567890")

    @pytest.mark.parametrize(
        "balance, amount, history, expected, expected_balance",
        [
            (300.0, 200.0, [-1775], False, 300.0),
            (400.0, 200.0, [-1675], False, 400.0),
            (400.0, 200.0, [-1775], True, 600.0),
        ],
    )
    def test_business_loan_small_balance(
        self, account, balance, amount, history, expected, expected_balance
    ):
        account.history = history
        account.balance = balance
        result = account.take_loan(amount)
        assert result is expected
        assert account.balance == expected_balance

from src.account import Account
import pytest


class TestLoan:

    @pytest.fixture()
    def account(self):
        return Account("John", "Doe", "12345678901")

    @pytest.mark.parametrize(
        "history, loan_amount, expected_result, expected_balance",
        [
            ([100, 200, 500], 200, True, 200),      #  dodatnie –  przyznana
            ([100, 200, 500, -100], 300, False, 0), #  jedna ujemna – odrzucona
        ],
    )
    def test_submit_for_loan_variants(
        self, account, history, loan_amount, expected_result, expected_balance
    ):
        account.history = history
        result = account.submit_for_loan(loan_amount)
        assert result is expected_result
        assert account.balance == expected_balance
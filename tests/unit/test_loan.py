from src.account import Account
import pytest

class TestLoan:

    @pytest.fixture()
    def account(self):
        a = Account("John", "Doe", "12345678901")
        return a

    def test_3_posiitve_transfers(self, account):
        account.history = [100, 200, 500]
        result =  account.submit_for_loan(200)
        assert result
        assert account.balance == 200
   
    def test_4_transfers_one_negative(self, account):
        account.history = [100, 200, 500, -100]
        result = account.submit_for_loan(300)
        assert result is False
        assert account.balance == 0
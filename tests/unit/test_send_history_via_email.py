from unittest.mock import patch

from src.account import Account
from src.business_account import BusinessAccount


class TestSendHistoryViaEmail:
    def test_personal_account_send_history_success(self):
        account = Account("Jan", "Kowalski", "30010112345")
        account.transfer_in(150.0)
        account.transfer_out(50.0)

        with patch("src.account.SMTPClient.send", return_value=True) as mock_send:
            result = account.send_history_via_email("test@email.com")

        assert result is True
        mock_send.assert_called_once()

        subject = mock_send.call_args[0][0]
        text = mock_send.call_args[0][1]
        email = mock_send.call_args[0][2]

        assert subject.startswith("Account Transfer History ")
        assert text == "Personal account history:[150.0, -50.0]"
        assert email == "test@email.com"

    def test_personal_account_send_history_failure(self):
        account = Account("Jan", "Kowalski", "30010112345")
        account.transfer_in(150.0)

        with patch("src.account.SMTPClient.send", return_value=False) as mock_send:
            result = account.send_history_via_email("test@email.com")

        assert result is False
        mock_send.assert_called_once()

    def test_business_account_send_history_success(self):
        with patch("src.business_account.BusinessAccount.is_nip_active_in_mf", return_value=True):
            account = BusinessAccount(company_name="FooBar", nip="1234567890")
            account.transfer_in(5000.0)
            account.transfer_out(1000.0)
            account.transfer_in(500.0)

            with patch("src.business_account.SMTPClient.send", return_value=True) as mock_send:
                result = account.send_history_via_email("test@email.com")

        assert result is True
        mock_send.assert_called_once()

        subject = mock_send.call_args[0][0]
        text = mock_send.call_args[0][1]
        email = mock_send.call_args[0][2]

        assert subject.startswith("Account Transfer History ")
        assert text == "Company account history:[5000.0, -1000.0, 500.0]"
        assert email == "test@email.com"

    def test_business_account_send_history_failure(self):
        with patch("src.business_account.BusinessAccount.is_nip_active_in_mf", return_value=True):
            account = BusinessAccount(company_name="FooBar", nip="1234567890")
            account.transfer_in(1.0)

            with patch("src.business_account.SMTPClient.send", return_value=False) as mock_send:
                result = account.send_history_via_email("test@email.com")

        assert result is False
        mock_send.assert_called_once()
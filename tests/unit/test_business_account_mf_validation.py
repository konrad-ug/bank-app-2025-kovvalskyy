import json
import pytest
from src.business_account import BusinessAccount


class DummyResponse:
    def __init__(self, status_code: int, payload: dict):
        self.status_code = status_code
        self._payload = payload
        self.text = json.dumps(payload)

    def json(self):
        return self._payload


class TestBusinessAccountMfValidation:
    def test_does_not_send_request_when_nip_has_wrong_length(self, mocker):
        get_mock = mocker.patch("src.business_account.requests.get")

        b = BusinessAccount(company_name="Foo", nip="123")
        assert b.nip == "123"

        get_mock.assert_not_called()

    def test_sends_request_when_nip_has_length_10_and_is_digit(self, mocker, capsys):
        mocker.patch.dict(
            "os.environ",
            {"BANK_APP_MF_URL": "https://example.test"},
            clear=False,
        )

        payload = {"result": {"subject": {"statusVat": "Czynny"}}}
        get_mock = mocker.patch(
            "src.business_account.requests.get",
            return_value=DummyResponse(200, payload),
        )

        b = BusinessAccount(company_name="Foo", nip="8461627563")
        assert b.nip == "8461627563"

        out = capsys.readouterr().out
        assert "statusVat" in out

        get_mock.assert_called_once()

    def test_constructor_raises_when_mf_status_is_not_czynny(self, mocker):
        payload = {"result": {"subject": {"statusVat": "Zwolniony"}}}
        mocker.patch(
            "src.business_account.requests.get",
            return_value=DummyResponse(200, payload),
        )

        with pytest.raises(ValueError) as err:
            BusinessAccount(company_name="Foo", nip="1111111111")

        assert str(err.value) == "Company not registered!!"
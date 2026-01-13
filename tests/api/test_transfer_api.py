import pytest
import requests


class TestTransferApi:
    BASE_URL = "http://127.0.0.1:5000"

    ACCOUNT = {
        "name": "John",
        "surname": "Doe",
        "pesel": "12345678901",
    }

    @pytest.fixture(autouse=True)
    def setup_and_cleanup(self):
        requests.delete(f"{self.BASE_URL}/api/accounts/{self.ACCOUNT['pesel']}")
        response = requests.post(
            f"{self.BASE_URL}/api/accounts",
            json=self.ACCOUNT
        )
        assert response.status_code == 201

        yield

        response = requests.get(f"{self.BASE_URL}/api/accounts")
        if response.status_code == 200:
            for acc in response.json():
                requests.delete(f"{self.BASE_URL}/api/accounts/{acc['pesel']}")

    def _get_balance(self, pesel):
        response = requests.get(f"{self.BASE_URL}/api/accounts/{pesel}")
        return response.json()["balance"]

    def test_returns_404_when_account_does_not_exist(self):
        response = requests.post(
            f"{self.BASE_URL}/api/accounts/00000000000/transfer",
            json={"amount": 100, "type": "incoming"},
        )
        assert response.status_code == 404
        assert response.json()["message"] == "Account not found"

    def test_returns_400_for_unknown_transfer_type(self):
        pesel = self.ACCOUNT["pesel"]
        response = requests.post(
            f"{self.BASE_URL}/api/accounts/{pesel}/transfer",
            json={"amount": 100, "type": "banana"},
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Unknown transfer type"

    def test_returns_400_for_invalid_amount(self):
        pesel = self.ACCOUNT["pesel"]
        response = requests.post(
            f"{self.BASE_URL}/api/accounts/{pesel}/transfer",
            json={"amount": "abc", "type": "incoming"},
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Invalid amount"

    def test_incoming_transfer_increases_balance(self):
        pesel = self.ACCOUNT["pesel"]
        before = self._get_balance(pesel)

        response = requests.post(
            f"{self.BASE_URL}/api/accounts/{pesel}/transfer",
            json={"amount": 500, "type": "incoming"},
        )

        assert response.status_code == 200
        assert response.json()["message"] == "Processing transfer"

        after = self._get_balance(pesel)
        assert after == before + 500

    def test_outgoing_transfer_decreases_balance(self):
        pesel = self.ACCOUNT["pesel"]

        requests.post(
            f"{self.BASE_URL}/api/accounts/{pesel}/transfer",
            json={"amount": 500, "type": "incoming"},
        )

        before = self._get_balance(pesel)

        response = requests.post(
            f"{self.BASE_URL}/api/accounts/{pesel}/transfer",
            json={"amount": 200, "type": "outgoing"},
        )

        assert response.status_code == 200

        after = self._get_balance(pesel)
        assert after == before - 200

    def test_outgoing_transfer_returns_422_when_insufficient_funds(self):
        pesel = self.ACCOUNT["pesel"]
        before = self._get_balance(pesel)

        response = requests.post(
            f"{self.BASE_URL}/api/accounts/{pesel}/transfer",
            json={"amount": before + 1, "type": "outgoing"},
        )

        assert response.status_code == 422
        assert response.json()["message"] == "Transfer rejected"

        after = self._get_balance(pesel)
        assert after == before

    def test_express_transfer_applies_fee(self):
        pesel = self.ACCOUNT["pesel"]

        requests.post(
            f"{self.BASE_URL}/api/accounts/{pesel}/transfer",
            json={"amount": 500, "type": "incoming"},
        )

        before = self._get_balance(pesel)

        response = requests.post(
            f"{self.BASE_URL}/api/accounts/{pesel}/transfer",
            json={"amount": 100, "type": "express"},
        )

        assert response.status_code == 200

        after = self._get_balance(pesel)
        assert after == before - 100 - 1.0
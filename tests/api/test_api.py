import pytest
import requests


class TestCrudApi:
    url = "http://127.0.0.1:5000"
    base_account = {
        "name": "John",
        "surname": "Doe",
        "pesel": "12345678901"
    }

    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self):
        requests.delete(f"{self.url}/api/accounts/{self.base_account['pesel']}")
        response = requests.post(f"{self.url}/api/accounts", json=self.base_account)
        assert response.status_code == 201
        yield
        response = requests.get(f"{self.url}/api/accounts")
        accounts = response.json()
        for account in accounts:
            pesel = account["pesel"]
            delete_response = requests.delete(f"{self.url}/api/accounts/{pesel}")
            assert delete_response.status_code == 200

    def test_get_account_count(self):
        for acc in requests.get(f"{self.url}/api/accounts").json():
            requests.delete(f"{self.url}/api/accounts/{acc['pesel']}")

        payload = {"name": "John", "surname": "Doe", "pesel": "12345678901"}
        r = requests.post(f"{self.url}/api/accounts", json=payload)
        assert r.status_code == 201

        response = requests.get(f"{self.url}/api/accounts/count")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1


    def test_create_account(self):
        new_account = {
            "name": "James",
            "surname": "Hetfield",
            "pesel": "89092909825"
        }
        response = requests.post(f"{self.url}/api/accounts", json=new_account)
        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Account created"

    def test_get_account_by_pesel(self):
        pesel = self.base_account["pesel"]
        response = requests.get(f"{self.url}/api/accounts/{pesel}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == self.base_account["name"]
        assert data["surname"] == self.base_account["surname"]
        assert data["pesel"] == pesel
        assert "balance" in data

    def test_get_account_by_pesel_returns_404_when_missing(self):
        response = requests.get(f"{self.url}/api/accounts/00000000000")
        assert response.status_code == 404
        data = response.json()
        assert data["message"] == "Account not found"

    def test_patch_update_account(self):
        pesel = self.base_account["pesel"]
        patch_data = {"name": "Kirk"}
        response = requests.patch(f"{self.url}/api/accounts/{pesel}", json=patch_data)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Account updated"
        response = requests.get(f"{self.url}/api/accounts/{pesel}")
        assert response.status_code == 200
        acc = response.json()
        assert acc["name"] == "Kirk"
        assert acc["surname"] == self.base_account["surname"]

    def test_delete_account(self):
        pesel_to_delete = self.base_account["pesel"]
        response = requests.delete(f"{self.url}/api/accounts/{pesel_to_delete}")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Account deleted"
        response = requests.get(f"{self.url}/api/accounts/{pesel_to_delete}")
        assert response.status_code == 404

    def test_create_account_with_already_existing_pesel(self):
        count_before = requests.get(f"{self.url}/api/accounts/count").json()["count"]
        response = requests.post(f"{self.url}/api/accounts", json=self.base_account)
        assert response.status_code == 409
        data = response.json()
        assert data["message"] == "Account with this PESEL already exists"
        count_after = requests.get(f"{self.url}/api/accounts/count").json()["count"]
        assert count_after == count_before


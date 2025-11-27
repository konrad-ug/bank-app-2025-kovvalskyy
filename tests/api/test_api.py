import pytest
import requests

class TestAPI:
    url = "http://127.0.0.1:5000/api/accounts"
    account_details = {
        "name": "John",
        "surname": "Doe",
        "pesel": "12345678901"
    }

    @pytest.fixture(autouse = True, scope="function")
    def set_up(self):
        response = requests.post(self.url, json=self.account_details)
        assert response.status_code == 201
        yield
        accounts = requests.get(self.url).json()
        for account in accounts:
            delete_response = requests.delete(f"{self.url}/{account['pesel']}")
            assert delete_response.status_code == 200
    
    def test_create_account(self): 
        response = requests.post(self.url, json = self.account_details)
        assert response.status_code == 201
        assert response.json()["message"] == "Account created"

    def test_get_account_count(self):
        link = self.url + "/count"
        response = requests.get(link)
        assert response.status_code == 200
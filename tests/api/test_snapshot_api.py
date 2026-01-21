import requests


class TestSnapshotApi:
    url = "http://127.0.0.1:5000"

    def test_save_and_load(self):
        payload = {"name": "John", "surname": "Doe", "pesel": "12345678901"}
        assert requests.post(f"{self.url}/api/accounts", json=payload).status_code == 201

        assert requests.post(f"{self.url}/api/accounts/save").status_code == 200

        assert requests.delete(f"{self.url}/api/accounts/12345678901").status_code == 200

        assert requests.post(f"{self.url}/api/accounts/load").status_code == 200
        assert requests.get(f"{self.url}/api/accounts/12345678901").status_code == 200

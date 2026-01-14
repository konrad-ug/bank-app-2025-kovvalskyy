import time
import requests

BASE_URL = "http://127.0.0.1:5000"
TIME_LIMIT = 0.5


def timed_request(method, url, **kwargs):
    start = time.perf_counter()
    resp = method(url, timeout=TIME_LIMIT, **kwargs)
    duration = time.perf_counter() - start
    assert duration < TIME_LIMIT
    return resp


def test_create_and_delete_account_100_times():
    for i in range(100):
        pesel = f"900000000{i:02d}"

        r1 = timed_request(
            requests.post,
            f"{BASE_URL}/api/accounts",
            json={"name": "Perf", "surname": "Test", "pesel": pesel},
        )
        assert r1.status_code == 201

        r2 = timed_request(
            requests.delete,
            f"{BASE_URL}/api/accounts/{pesel}",
        )
        assert r2.status_code == 200


def test_create_account_and_100_incoming_transfers_balance():
    pesel = "91111111111"

    r1 = timed_request(
        requests.post,
        f"{BASE_URL}/api/accounts",
        json={"name": "Perf", "surname": "Transfer", "pesel": pesel},
    )
    assert r1.status_code == 201

    amount = 10
    for _ in range(100):
        r = timed_request(
            requests.post,
            f"{BASE_URL}/api/accounts/{pesel}/transfer",
            json={"amount": amount, "type": "incoming"},
        )
        assert r.status_code == 200

    acc = timed_request(requests.get, f"{BASE_URL}/api/accounts/{pesel}")
    assert acc.status_code == 200
    assert acc.json()["balance"] == 100 * amount
from src.account import Account
from src.repositories.mongo_accounts_repository import MongoAccountsRepository


def test_load_all_uses_mock_find(mocker):
    mock_collection = mocker.Mock()
    mock_collection.find.return_value = [
        {
            "first_name": "John",
            "last_name": "Doe",
            "pesel": "12345678901",
            "balance": 100.0,
            "history": [100.0],
        }
    ]

    repo = MongoAccountsRepository()
    repo._collection = mock_collection

    accounts = repo.load_all()
    assert len(accounts) == 1
    assert isinstance(accounts[0], Account)
    assert accounts[0].pesel == "12345678901"

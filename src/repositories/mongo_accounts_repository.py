from pymongo import MongoClient
from src.account import Account


class MongoAccountsRepository:
    def __init__(self):
        self._client = MongoClient("mongodb://localhost:27017")
        self._collection = self._client["bank_app"]["accounts"]

    def save_all(self, accounts):
        # przed zapisem czyścimy kolekcję
        self._collection.delete_many({})
        for account in accounts:
            self._collection.update_one(
                {"pesel": account.pesel},
                {"$set": account.to_dict()},
                upsert=True,
            )

    def load_all(self):
        docs = self._collection.find({})
        accounts = []
        for doc in docs:
            doc.pop("_id", None)
            accounts.append(Account.from_dict(doc))
        return accounts

import pytest
from src.account import Account
from src.account_registry import AccountRegistry

class TestAccountRegsitry:

    @pytest.fixture
    def sample_accounts(self):
        return [
            Account("John", "Doe", "12345678901"),
            Account("Jane", "Smith", "98765432109"),
            Account("Alice", "Brown", "11111111111"),
        ]

    @pytest.fixture
    def empty_registry(self):
        return AccountRegistry()
    
    def test_add_account_to_list(self, empty_registry):
        acc = Account("John", "Doe", "12345678901")

        result = empty_registry.add_account(acc)

        assert result is True
        assert empty_registry.show_registry()[0] is acc

    def test_search_account_by_pesel_found(self, empty_registry, sample_accounts):
        for acc in sample_accounts:
            empty_registry.add_account(acc)

        pesel_to_find = sample_accounts[1].pesel

        found = empty_registry.search_account(pesel_to_find)

        assert found is not None
        assert found is sample_accounts[1]
        assert found.first_name == "Jane"
        assert found.last_name == "Smith"

    def test_search_account_by_pesel_not_found(self, empty_registry, sample_accounts):
        for acc in sample_accounts:
            empty_registry.add_account(acc)

        not_existing_pesel = "99999999999"

        found = empty_registry.search_account(not_existing_pesel)

        assert found is None

    def test_show_registry_returns_all_accounts(self, empty_registry, sample_accounts):
        for acc in sample_accounts:
            empty_registry.add_account(acc)

        registry_list = empty_registry.show_registry()

        assert registry_list == sample_accounts

    def test_count_accounts(self, empty_registry, sample_accounts):
        for acc in sample_accounts:
            empty_registry.add_account(acc)

        assert empty_registry.count_accounts() == len(sample_accounts)

    def test_delete_non_existing_account_returns_false(self):
        reg = AccountRegistry()
        assert reg.delete_account("12345678901") is False

    def test_add_account_returns_false_when_pesel_already_exists(self, empty_registry):
        acc1 = Account("John", "Doe", "12345678901")
        acc2 = Account("Jane", "Smith", "12345678901")

        assert empty_registry.add_account(acc1) is True
        assert empty_registry.count_accounts() == 1
        assert empty_registry.add_account(acc2) is False
        assert empty_registry.count_accounts() == 1
        assert empty_registry.search_account("12345678901") is acc1
    
    def test_delete_existing_account_returns_true_and_removes(self, empty_registry):
        acc = Account("John", "Doe", "12345678901")
        assert empty_registry.add_account(acc) is True

        assert empty_registry.delete_account("12345678901") is True
        assert empty_registry.search_account("12345678901") is None
        assert empty_registry.count_accounts() == 0
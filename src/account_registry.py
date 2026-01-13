from src.account import Account

class AccountRegistry:
    
    def __init__(self):
        self.accounts = []
    
    def add_account(self, account: Account):
        if self.search_account(account.pesel) is not None:
            return False
        self.accounts.append(account)
        return True

    def search_account(self, pesel):
        for acc in self.accounts:
            if acc.pesel == pesel:
                return acc
        return None
    
    def show_registry(self):
        return self.accounts

    def count_accounts(self):
        return len(self.accounts)
    
    def delete_account(self, pesel) -> bool:
        account = self.search_account(pesel)
        if account is None:
            return False
        self.accounts.remove(account)
        return True
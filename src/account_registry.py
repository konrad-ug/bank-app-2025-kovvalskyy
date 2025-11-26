from src.account import Account

class AccountRegistry:
    
    def __init__(self):
        self.accounts = []
    
    def add_account(self, account: Account):
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
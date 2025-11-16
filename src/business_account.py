class BusinessAccount:
    def __init__(self, company_name: str, nip: str):
        self.company_name = company_name
        self.nip = nip if self._is_nip_valid(nip) else "Invalid"
        self.balance = 0.0
        self.history = []

    def _is_nip_valid(self, nip):
        return isinstance(nip, str) and len(nip) == 10 and nip.isdigit()

    def _is_positive(self, amount):
        try:
            return isinstance(amount, (int, float)) and amount > 0
        except Exception:
            return False

    def can_transfer_out(self, amount: float):
        return self._is_positive(amount) and self.balance >= float(amount)

    def transfer_in(self, amount: float):
        if not self._is_positive(amount):
            return False
        self.balance += float(amount)
        self.history.append(float(amount))
        return True

    def transfer_out(self, amount: float):
        if not self.can_transfer_out(amount):
            return False
        self.balance -= float(amount)
        self.history.append(-float(amount))
        return True

    def express_out(self, amount: float):
        fee = 5.0
        if not self._is_positive(amount):
            return False
        if self.balance < float(amount):
            return False
        self.balance -= float(amount)
        self.history.append(-float(amount))
        self.balance -= fee
        self.history.append(-fee)
        return True

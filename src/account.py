class Account:
    def __init__(self, first_name, last_name, pesel, promoCode=None):
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.balance = 50 if self.is_promoCode_valid(promoCode) and self.is_person_using_promoCode_valid(pesel) else 0.0

    def is_pesel_valid(self, pesel):
        if isinstance(pesel, str) and len(pesel) == 11:
            return True
        
    def is_promoCode_valid(self, promoCode):
        if promoCode is not None and promoCode.startswith("PROM_") and len(promoCode) == 8:
            return True

    def is_person_using_promoCode_valid(self, pesel):
        year = int(pesel[0:2])
        month = int(pesel[2:4])
        if year > 60 or month > 20:
            return True
    
    def _is_positive(self, amount):
        try:
            return isinstance(amount, (int, float)) and amount > 0
        except Exception:
            return False

    def transfer_in(self, amount: float):
        if not self._is_positive(amount):
            return False
        self.balance += float(amount)
        return True

    def can_transfer_out(self, amount: float):
        return self._is_positive(amount) and self.balance >= float(amount)

    def transfer_out(self, amount: float):
        if not self.can_transfer_out(amount):
            return False
        self.balance -= float(amount)
        return True

    def express_out(self, amount: float):
        fee = 1.0
        if not self._is_positive(amount):
            return False
        if self.balance < float(amount):
            return False
        
        self.balance -= float(amount)
        self.balance -= fee
        return True

class BusinessAccount:
    def __init__(self, company_name: str, nip: str, promoCode=None):
        self.company_name = company_name
        self.nip = nip if self._is_nip_valid(nip) else "Invalid"
        self.balance = 0.0

    def _is_positive(self, amount):
        try:
            return isinstance(amount, (int, float)) and amount > 0
        except Exception:
            return False

    def _is_nip_valid(self, nip):
        return isinstance(nip, str) and len(nip) == 10 and nip.isdigit()

    def transfer_in(self, amount: float):
        if not self._is_positive(amount):
            return False
        self.balance += float(amount)
        return True

    def can_transfer_out(self, amount: float):
        return self._is_positive(amount) and self.balance >= float(amount)

    def transfer_out(self, amount: float):
        if not self.can_transfer_out(amount):
            return False
        self.balance -= float(amount)
        return True

    def express_out(self, amount: float):
        fee = 5.0
        if not self._is_positive(amount):
            return False
        if self.balance < float(amount):
            return False
        self.balance -= float(amount)
        self.balance -= fee
        return True
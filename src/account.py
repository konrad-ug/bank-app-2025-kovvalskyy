from datetime import date
from src.smtp.smtp import SMTPClient

class Account:
    def __init__(self, first_name, last_name, pesel, promoCode=None):
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.balance = 50 if self.is_promoCode_valid(promoCode) and self.is_person_using_promoCode_valid(pesel) else 0.0
        self.history = []

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
            return float(amount) > 0
        except (TypeError, ValueError):
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
        fee = 1.0
        if not self._is_positive(amount):
            return False
        if self.balance < float(amount):
            return False
        self.balance -= float(amount)
        self.history.append(-float(amount))
        self.balance -= fee
        self.history.append(-fee)
        return True

    def submit_for_loan(self, amount: float):
        last3_incoming = len(self.history) >= 3 and all(x > 0 for x in self.history[-3:])
        last5_sum_ok = len(self.history) >= 5 and sum(self.history[-5:]) > amount

        if last3_incoming or last5_sum_ok:
            self.balance += amount
            return True
        return False

    def send_history_via_email(self, email_address: str) -> bool:
        today = date.today().isoformat()
        subject = f"Account Transfer History {today}"
        text = f"Personal account history:{self.history}"
        return SMTPClient.send(subject, text, email_address)
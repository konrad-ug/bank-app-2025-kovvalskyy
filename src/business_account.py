import os
from datetime import date
from src.smtp.smtp import SMTPClient

import requests


class BusinessAccount:  # pragma: no cover
    def __init__(self, company_name: str, nip: str):  # pragma: no cover
        self.company_name = company_name
        self.nip = nip
        if not (isinstance(nip, str) and len(nip) == 10 and nip.isdigit()):
            self.nip = "Invalid"
        self.balance = 0.0
        self.history = []

        if isinstance(nip, str) and len(nip) == 10 and nip.isdigit():
            if not self.is_nip_active_in_mf(nip):
                raise ValueError("Company not registered!!")

    @staticmethod
    def _mf_base_url() -> str:  # pragma: no cover
        return os.getenv("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl/")

    @classmethod
    def is_nip_active_in_mf(cls, nip: str) -> bool:  # pragma: no cover
        base = cls._mf_base_url().rstrip("/")
        today = date.today().isoformat()  # YYYY-MM-DD
        url = f"{base}/api/search/nip/{nip}?date={today}"

        try:
            resp = requests.get(url, timeout=10)
            print(resp.text)

            if resp.status_code != 200:
                return False

            payload = resp.json()
        except Exception:
            return False

        subject = payload.get("result", {}).get("subject")
        if not isinstance(subject, dict):
            return False

        return subject.get("statusVat") == "Czynny"

    def _is_positive(self, amount):  # pragma: no cover
        try:
            return isinstance(amount, (int, float)) and amount > 0
        except Exception:
            return False

    def can_transfer_out(self, amount: float):  # pragma: no cover
        return self._is_positive(amount) and self.balance >= float(amount)

    def transfer_in(self, amount: float):  # pragma: no cover
        if not self._is_positive(amount):
            return False
        self.balance += float(amount)
        self.history.append(float(amount))
        return True

    def transfer_out(self, amount: float):  # pragma: no cover
        if not self.can_transfer_out(amount):
            return False
        self.balance -= float(amount)
        self.history.append(-float(amount))
        return True

    def express_out(self, amount: float):  # pragma: no cover
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
    
    def take_loan(self, amount: float):  # pragma: no cover
        zus = -1775
        if self.balance >= amount*2 and zus in self.history:
            self.balance += amount
            return True
        return False
    
    def send_history_via_email(self, email_address: str) -> bool:
        today = date.today().isoformat()
        subject = f"Account Transfer History {today}"
        text = f"Company account history:{self.history}"
        return SMTPClient.send(subject, text, email_address)
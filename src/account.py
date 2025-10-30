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
from src.account import Account, BusinessAccount

class TestHistory:
    def test_history_personal_in_out_express(self):
        a = Account("John", "Doe", "12345678901")
        assert hasattr(a, "historia")
        a.transfer_in(500.0)
        a.express_out(300.0)
        assert a.historia == [500.0, -300.0, -1.0]

    def test_history_business(self):
        b = BusinessAccount("Acme", "1234567890")
        assert hasattr(b, "historia")
        b.transfer_in(200.0)
        b.transfer_out(50.0)
        b.express_out(100.0)
        assert b.historia == [200.0, -50.0, -100.0, -5.0]
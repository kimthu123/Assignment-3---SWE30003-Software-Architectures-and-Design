from domain.account import Account

class Staff(Account):
    def __init__(self, email, password):
        super().__init__(email, password, account_type="staff")


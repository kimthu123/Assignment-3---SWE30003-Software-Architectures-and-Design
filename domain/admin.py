from domain.account import Account

class Admin(Account):
    def __init__(self, email, password):
        super().__init__(email, password, account_type="admin")


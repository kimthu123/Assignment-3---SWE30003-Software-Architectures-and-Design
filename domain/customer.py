from domain.account import Account

class Customer(Account):
    def __init__(self, email, password):
        super().__init__(email, password, account_type="customer")


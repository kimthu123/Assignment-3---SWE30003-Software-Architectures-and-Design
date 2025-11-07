"""Admin account module."""

from domain.account import Account


class Admin(Account):
    """Administrator account class."""

    def __init__(self, email, password):
        super().__init__(email, password, account_type="admin")

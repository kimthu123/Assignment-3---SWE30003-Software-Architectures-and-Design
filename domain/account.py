"""Account base class module."""


class Account:
    """Base class representing a system account."""

    def __init__(self, email, password, account_type):
        self.email = email
        self.password = password
        self.account_type = account_type

"""Defines the Staff class, which inherits from Account."""

from domain.account import Account


class Staff(Account):
    """Represents a staff account in the system."""

    def __init__(self, email, password):
        """Initialize a staff account with email and password."""
        super().__init__(email, password, account_type="staff")

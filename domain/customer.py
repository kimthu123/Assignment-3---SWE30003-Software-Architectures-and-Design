"""Customer account model."""

from domain.account import Account


class Customer(Account):
    """Represents a customer account type."""

    def __init__(self, email, password):
        """Initialize a customer account."""
        super().__init__(email, password, account_type="customer")

"""Handles packaging process for customer orders."""

import datetime

from utils.db_handler import read_json, write_json


class Packaging:
    """Represents the packaging process for an order."""

    def __init__(self, order_id):
        """Initialize packaging with associated order ID."""
        self.order_id = order_id

    def prepare_package(self):
        """Prepare a package record and save it to the data file."""
        packages = read_json('data/packages.json')
        package_id = len(packages) + 1

        package = {
            "package_id": package_id,
            "order_id": self.order_id,
            "status": "packed",
            "packed_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        packages.append(package)
        write_json('data/packages.json', packages)

        return {
            "message": f"Order {self.order_id} packaged successfully.",
            "package": package,
        }

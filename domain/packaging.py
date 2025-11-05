from utils.db_handler import read_json, write_json
import datetime

class Packaging:
    def __init__(self, order_id):
        self.order_id = order_id

    def prepare_package(self):
        packages = read_json('data/packages.json')
        package_id = len(packages) + 1

        package = {
            "package_id": package_id,
            "order_id": self.order_id,
            "status": "packed",
            "packed_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        packages.append(package)
        write_json('data/packages.json', packages)

        return {
            "message": f"Order {self.order_id} packaged successfully.",
            "package": package
        }

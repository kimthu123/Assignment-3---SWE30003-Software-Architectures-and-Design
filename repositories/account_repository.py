from utils.db_handler import read_json, write_json

class AccountRepository:
    def __init__(self):
        self.file_path = 'data/users.json'

    def get_data(self):
        return read_json(self.file_path)

    def get_id(self, account_id):
        accounts = read_json(self.file_path)
        return next((acc for acc in accounts if acc['id'] == account_id), None)

    def get_email(self, email):
        accounts = read_json(self.file_path)
        return next((acc for acc in accounts if acc['email'] == email), None)

    def save_all(self, accounts):
        write_json(self.file_path, accounts)

    def save(self, account_data):
        accounts = read_json(self.file_path)
        accounts.append(account_data)
        write_json(self.file_path, accounts)
        return account_data


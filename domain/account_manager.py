from domain.customer import Customer
from domain.admin import Admin
from domain.staff import Staff
from repositories.account_repository import AccountRepository

class AccountManager:
    def __init__(self):
        self.account_repo = AccountRepository()

    def load_all_accounts(self):
        # loads all accounts from repository
        return self.account_repo.get_data()

    def create_account(self, email, password, account_type=None):
        # create new account
        # check if email already exists
        if self.account_repo.get_email(email):
            return {"error": "Email already exists"}
        
        # designate account type based on domain
        if account_type is None:
            if email.endswith("@localstoreadmin.com.au"):
                account_type = "admin"
            elif email.endswith("@localstore.com.au"):
                account_type = "staff"
            else:
                account_type = "customer"
        
        if account_type == 'customer':
            account = Customer(email, password)
        elif account_type == 'admin':
            account = Admin(email, password)
        elif account_type == 'staff':
            account = Staff(email, password)
        else:
            return {"error": "Invalid account type"}
        
        # save to repository
        existing_accounts = self.account_repo.get_data()
        account_id = len(existing_accounts) + 1
        
        account_data = {
            "id": account_id,
            "email": email,
            "password": password,
            "account_type": account_type
        }
        
        self.account_repo.save(account_data)
        
        return {
            "message": "Account created successfully",
            "account_type": account_type
        }

    def delete_account(self, email):
        # delete account by email
        accounts = self.account_repo.get_data()
        account = next((account for account in accounts if account['email'] == email), None)
        
        if not account:
            return {"error": "Account not found"}
        
        # remove from repository
        accounts = [account for account in accounts if account['email'] != email]
        self.account_repo.save_all(accounts)
        
        return {"message": f"Account {email} deleted successfully"}

    def update_account(self, email, new_email=None, new_password=None):
        # update account information
        accounts = self.account_repo.get_data()
        account = next((account for account in accounts if account['email'] == email), None)
        
        if not account:
            return {"error": "Account not found"}
        
        if new_email:
            account['email'] = new_email
        if new_password:
            account['password'] = new_password
        
        self.account_repo.save_all(accounts)
        return {"message": "Account updated successfully"}

    def login(self, email, password):
        # authenticate user
        account_data = self.account_repo.get_email(email)
        
        if not account_data:
            return {"error": "Invalid email or password"}
        
        if account_data['password'] != password:
            return {"error": "Invalid email or password"}
        
        return {
            "message": "Login successful",
            "account": {
                "email": account_data['email'],
                "account_type": account_data['account_type']
            }
        }


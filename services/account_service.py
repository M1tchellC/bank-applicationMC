from models.account import Account


class AccountService:

    ## Receive the AccountRepository instance from main.py, so AccountService can call its data access methods

    def __init__(self, account_repository):
        self.account_repository = account_repository

    def create_account(self, user_id, account_type):

        # Check if account type is valid

        if not isinstance(account_type, str):
            raise ValueError("Account type must be CHECKING or SAVINGS")

        account_type = account_type.strip().upper()

        if account_type not in ["CHECKING", "SAVINGS"]:
            raise ValueError("Account type must be CHECKING or SAVINGS")

        account = Account(user_id, account_type)

        return self.account_repository.save(account)

    def get_account(self, account_id):

        ## get account by id from repository

        account = self.account_repository.get_by_id(account_id)

        if account is None:
            raise ValueError("Account not found")

        return account

    def get_all_accounts(self):

        ## get all accounts from repository

        return self.account_repository.get_all()
from models.account import Account


class AccountService:
    def __init__(self, account_repository):
        self.account_repository = account_repository

    def create_account(self, user_id, account_type):

        # Check if account type is valid

        account_type = account_type.upper()
        
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
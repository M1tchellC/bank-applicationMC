from models.account import Account


class AccountRepository:
    def __init__(self):
        # Temporary hard-coded data
        self.accounts = [
            Account(
                user_id=1,
                account_type="CHECKING",
                balance=1000.00,
                account_id=1,
            ),
            Account(
                user_id=2,
                account_type="SAVINGS",
                balance=500.00,
                account_id=2,
            ),
            Account(
                user_id=3,
                account_type="CHECKING",
                balance=750.00,
                account_id=3,
            ),
        ]

    def save(self, account):
        # Find the largest existing ID, then add one
        if self.accounts:
            account.account_id = max(
                existing_account.account_id
                for existing_account in self.accounts
            ) + 1
        else:
            account.account_id = 1

        self.accounts.append(account)
        return account

    def get_by_id(self, account_id):
        ## Get an account by its ID

        for account in self.accounts:
            if account.account_id == account_id:
                return account

        return None

    def get_all(self):

        ## Return all accounts in the repository

        return self.accounts

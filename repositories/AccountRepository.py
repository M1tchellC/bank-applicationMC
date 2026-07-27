class AccountRepository:
    def __init__(self):

        ## array to hold list of accounts

        self.accounts = []

    def save(self, account):

        ## assign account id to account based on length of accounts list

        account.account_id = len(self.accounts) + 1

        ## add account to array/list of accounts

        self.accounts.append(account)

        return account

    def get_by_id(self, account_id):

        ## loop through accounts and return account with matching id

        for account in self.accounts:
            if account.account_id == account_id:
                return account

        return None
from repositories.AccountRepository import AccountRepository
from services.account_service import AccountService


## create an instance of the account repository class

repo = AccountRepository()

## create the account service and give it access to the repository

service = AccountService(account_repository=repo)


## display the temporary hard-coded accounts

print("Accounts:")

for account in service.get_all_accounts():
    print(f"Account ID: {account.account_id}")
    print(f"User ID: {account.user_id}")
    print(f"Account Type: {account.account_type}")
    print(f"Balance: ${account.balance:.2f}")
    print()

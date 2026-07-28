from repositories.AccountRepository import AccountRepository
from services.account_service import AccountService
from repositories.UserRepository import UserRepository

## create an instance of the account repository class

account_repo = AccountRepository()

## create an instance of the user repository class

user_repo = UserRepository()

## create the account service and give it access to the repository

service = AccountService(account_repository=account_repo)


## display the temporary hard-coded accounts

print("Accounts:")

for account in service.get_all_accounts():
    print(f"Account ID: {account.account_id}")
    print(f"User ID: {account.user_id}")
    print(f"Account Type: {account.account_type}")
    print(f"Balance: ${account.balance:.2f}")
    print()

from fastapi import FastAPI, HTTPException
from repositories.AccountRepository import AccountRepository
from services.account_service import AccountService

app = FastAPI()

repository = AccountRepository()
service = AccountService(repository)
repository2 = TransactionRepository()
service2 = TransactionService(repository2)

#Account

@app.get("/accounts")
def get_accounts():
    return service.get_all_accounts()


@app.get("/accounts/{account_id}")
def get_account(account_id: int):
    try:
        return service.get_account(account_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@app.post("/accounts")
def create_account(user_id: int, account_type: str):
    try:
        return service.create_account(user_id, account_type)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


#Transaction

@app.get("/transactions")
def get_transactions():
    return service2.get_all_transactions()


@app.get("/transactions/{txn_id}")
def get_transaction(txn_id: int):
    try:
        return service2.get_transaction(txn_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@app.post("/transactions")
def create_transaction(txn_id: int, txn_type: str, account_id: int):
    try:
        return service2.create_transaction(txn_id, txn_type, account_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


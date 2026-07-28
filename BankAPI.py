from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from repositories.AccountRepository import AccountRepository
from repositories.TransactionRepository import TransactionRepository
from services.account_service import AccountService
from services.transaction_service import TransactionService

app = FastAPI()

account_repository = AccountRepository()
account_service = AccountService(account_repository)

transaction_repository = TransactionRepository()
transaction_service = TransactionService(account_repository, transaction_repository)


class AmountRequest(BaseModel):
    amount: float

#Account

@app.get("/accounts")
def get_accounts():
    return account_service.get_all_accounts()


@app.get("/accounts/{account_id}")
def get_account(account_id: int):
    try:
        return account_service.get_account(account_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@app.post("/accounts")
def create_account(user_id: int, account_type: str):
    try:
        return account_service.create_account(user_id, account_type)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


#Transaction

@app.post("/accounts/{account_id}/deposit")
def deposit(account_id: int, body: AmountRequest):
    try:
        return transaction_service.deposit(account_id, body.amount)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: int, body: AmountRequest):
    try:
        return transaction_service.withdraw(account_id, body.amount)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.get("/accounts/{account_id}/transactions")
def get_transactions(account_id: int):
    try:
        return transaction_service.get_transactions(account_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


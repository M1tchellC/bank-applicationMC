from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from repositories.AccountRepository import AccountRepository
from repositories.TransactionRepository import TransactionRepository
from repositories.UserRepository import UserRepository
from models.user import User

from services.account_service import AccountService
from services.transaction_service import TransactionService



app = FastAPI()

user_repository = UserRepository()

account_repository = AccountRepository()
account_service = AccountService(account_repository, user_repository)

transaction_repository = TransactionRepository()
transaction_service = TransactionService(account_repository, transaction_repository)


class AmountRequest(BaseModel):
    amount: float


class CreateUserRequest(BaseModel):
    name: str
    email: str


def _serialize_user(user):
    return {
        "userId": user.user_id,
        "name": user.name,
        "email": user.email,
        "createdAt": user.created_at,
    }


@app.get("/users")
def get_users():
    users = user_repository.get_all()
    return [_serialize_user(user) for user in users]


@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = user_repository.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return _serialize_user(user)


@app.post("/users")
def create_user(body: CreateUserRequest):
    user = User(name=body.name.strip(), email=body.email.strip())
    saved_user = user_repository.save(user)
    return _serialize_user(saved_user)

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


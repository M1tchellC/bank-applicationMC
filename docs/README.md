# Bank Application

A simple banking system for learning backend architecture and service-layer business rules.

## Features

- Create an account
- View account details
- Deposit money
- Withdraw money
- View transaction history

## Current Implementation

This repository now uses MongoDB repositories for persistence.

- AccountRepository reads and writes account data in MongoDB
- UserRepository reads and writes user data in MongoDB
- TransactionRepository reads and writes transaction data in MongoDB
- TransactionService contains deposit and withdraw validation and business logic

## Project Structure

```
models/
    account.py
    user.py
    transaction.py

repositories/
    AccountRepository.py
    UserRepository.py
    TransactionRepository.py
    mongo.py

services/
    account_service.py
    transaction_service.py

BankAPI.py
main.py
```

## Architecture

1. API layer receives request
2. Service layer applies business rules
3. Repository layer stores and retrieves data
4. Model layer defines data objects

## Business Rules

- Deposit amount must be a valid positive number
- Withdraw amount must be a valid positive number
- Cannot withdraw more than current account balance
- Every successful deposit and withdraw creates a transaction record
- Passwords are stored only as Argon2 hashes
- Account and transaction routes require a valid JWT access token
- An authenticated user can access only their own accounts

## Quick Start

### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure MongoDB

```bash
cp .env.example .env
```

Set the following values in `.env`:

- MONGODB_URI (Atlas connection string)
- MONGODB_DB_NAME (example: bank_application)
- JWT_SECRET_KEY (a random value of at least 32 characters)

For local development, the API can instead read the secret from an ignored
`.jwt-secret` file generated with `openssl rand -hex -out .jwt-secret 32`.

Optional values:

- MONGODB_USERS_COLLECTION
- MONGODB_ACCOUNTS_COLLECTION
- MONGODB_TRANSACTIONS_COLLECTION

### 4. Run the API

```bash
uvicorn BankAPI:app --reload
```

### 5. Test with real MongoDB entries

After configuring `.env`, run the smoke test from the project root:

```bash
python scripts/mongodb_smoke_test.py
```

The test connects to the configured database and leaves behind one uniquely named
sample user, one checking account, a deposit, and a withdrawal. It verifies that
the final balance is `100.25` and that both transaction records can be read back.

You can inspect the entries in MongoDB Atlas under **Database > Browse Collections**,
or start the API and use its interactive documentation at:

```text
http://127.0.0.1:8000/docs
```

## Test JWT authentication without a frontend

Start the API and open `http://127.0.0.1:8000/docs`.

1. Use `POST /auth/register` with a name, email, and password of at least 12 characters.
2. Click the **Authorize** button at the top of Swagger.
3. Enter the registered email in the `username` field and the password in the `password` field. Leave client ID and client secret empty.
4. Swagger stores the returned bearer token and sends it with protected requests.
5. Use `GET /auth/me` to confirm the authenticated identity.
6. Create an account with `POST /accounts`; the owner comes from the JWT.
7. Test deposits, withdrawals, and transaction history with the returned account ID.
8. Click **Authorize**, then **Logout**, and confirm that protected routes return `401`.

Existing database users created before authentication do not have password hashes and
cannot log in. Register a new test user for the JWT flow.

## API Endpoints

### Accounts

- GET /accounts
- GET /accounts/{account_id}
- POST /accounts

### Authentication

- POST /auth/register
- POST /auth/token
- GET /auth/me

### Transactions

- POST /accounts/{account_id}/deposit
- POST /accounts/{account_id}/withdraw
- GET /accounts/{account_id}/transactions

## Team Notes

- Keep repository classes focused on data access only
- Keep service classes focused on validation and business logic only
- Keep credentials in environment variables and do not commit `.env`

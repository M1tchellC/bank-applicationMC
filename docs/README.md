# Bank Application

A simple banking system for learning backend architecture and service-layer business rules.

## Features

- Create an account
- View account details
- Deposit money
- Withdraw money
- View transaction history

## Current Implementation

This repository currently uses **hard-coded in-memory repositories** (no persistent DB writes in the main flow).

- `AccountRepository` manages account data in memory
- `UserRepository` manages user data in memory
- `TransactionRepository` manages transaction data in memory
- `TransactionService` contains deposit/withdraw validation and business logic

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

services/
	account_service.py
	transaction_service.py

BankAPI.py
main.py
```

## Architecture (MVC-style layering)

1. Controller/API layer receives request
2. Service layer applies business rules
3. Repository layer stores/retrieves data
4. Model layer defines data objects

## Business Rules

- Deposit amount must be a valid positive number
- Withdraw amount must be a valid positive number
- Cannot withdraw more than current account balance
- Every successful deposit/withdraw creates a transaction record

## Quick Start

### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install fastapi uvicorn
```

### 3. Run the API

```bash
uvicorn BankAPI:app --reload
```

## API Endpoints

### Accounts

- `GET /accounts` - Get all accounts
- `GET /accounts/{account_id}` - Get account by ID
- `POST /accounts` - Create account

### Transactions

- `GET /transactions` - Get all transactions
- `GET /transactions/{txn_id}` - Get transaction by ID
- `POST /transactions` - Create transaction entry

## Example Request Payloads

### Create Account

```json
{
	"user_id": 1,
	"account_type": "SAVINGS"
}
```

### Deposit (service-level method)

```json
{
	"account_id": 1,
	"amount": 250.0
}
```

### Withdraw (service-level method)

```json
{
	"account_id": 1,
	"amount": 125.0
}
```

## Team Notes

- Keep repository classes focused on data access only
- Keep service classes focused on validation/business logic only
- This in-memory version is ideal for demos and unit tests
- For production, replace repository internals with database queries

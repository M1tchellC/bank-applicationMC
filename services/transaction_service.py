from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any

from models.transaction import Transaction


class TransactionService:
    # Receive repository instances from main.py, same style as AccountService.
    def __init__(self, account_repository, transaction_repository):
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository

    def _validate_account_id(self, account_id: int) -> int:
        if not isinstance(account_id, int) or account_id <= 0:
            raise ValueError("Account ID must be a positive integer")
        return account_id

    def _validate_amount(self, amount: Any) -> Decimal:
        # Convert through string so both 12.5 and "12.5" are accepted.
        try:
            validated_amount = Decimal(str(amount))
        except (InvalidOperation, TypeError, ValueError):
            raise ValueError("Amount must be a valid number")

        if validated_amount <= 0:
            raise ValueError("Amount must be greater than zero")

        # Keep money values to 2 decimal places.
        return validated_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def deposit(self, account_id: int, amount: Any):
        """Add money to an account and create a matching deposit transaction."""
        validated_account_id = self._validate_account_id(account_id)
        validated_amount = self._validate_amount(amount)

        account = self.account_repository.get_by_id(validated_account_id)
        if account is None:
            raise ValueError("Account not found")

        current_balance = Decimal(str(account.balance))
        updated_balance = current_balance + validated_amount
        account.balance = float(updated_balance)

        transaction = Transaction(
            account_id=validated_account_id,
            transaction_type="DEPOSIT",
            amount=float(validated_amount),
        )
        saved_transaction = self.transaction_repository.save(transaction)

        return {
            "accountId": account.account_id,
            "previousBalance": float(current_balance),
            "balance": float(updated_balance),
            "transaction": {
                "transactionId": saved_transaction.transaction_id,
                "accountId": saved_transaction.account_id,
                "type": saved_transaction.transaction_type,
                "amount": saved_transaction.amount,
                "date": saved_transaction.created_at,
            },
        }

    def withdraw(self, account_id: int, amount: Any):
        """Remove money from an account and create a matching withdrawal transaction."""
        validated_account_id = self._validate_account_id(account_id)
        validated_amount = self._validate_amount(amount)

        account = self.account_repository.get_by_id(validated_account_id)
        if account is None:
            raise ValueError("Account not found")

        current_balance = Decimal(str(account.balance))
        if validated_amount > current_balance:
            raise ValueError("Insufficient balance. Cannot withdraw more than current balance")

        updated_balance = current_balance - validated_amount
        account.balance = float(updated_balance)

        transaction = Transaction(
            account_id=validated_account_id,
            transaction_type="WITHDRAW",
            amount=float(validated_amount),
        )
        saved_transaction = self.transaction_repository.save(transaction)

        return {
            "accountId": account.account_id,
            "previousBalance": float(current_balance),
            "balance": float(updated_balance),
            "transaction": {
                "transactionId": saved_transaction.transaction_id,
                "accountId": saved_transaction.account_id,
                "type": saved_transaction.transaction_type,
                "amount": saved_transaction.amount,
                "date": saved_transaction.created_at,
            },
        }

    def get_transactions(self, account_id: int):
        """Return transaction history for one account."""
        validated_account_id = self._validate_account_id(account_id)

        account = self.account_repository.get_by_id(validated_account_id)
        if account is None:
            raise ValueError("Account not found")

        transactions = self.transaction_repository.get_by_account_id(validated_account_id)
        return [
            {
                "transactionId": txn.transaction_id,
                "accountId": txn.account_id,
                "type": txn.transaction_type,
                "amount": txn.amount,
                "date": txn.created_at,
            }
            for txn in transactions
        ]
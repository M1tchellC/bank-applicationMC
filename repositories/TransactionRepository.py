from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any

# db connection helper used to open/close mysql connections
from python_backend.config.db import get_db_connection

# repositories are responsible for raw data access (select/update/insert)
from python_backend.repositories import account_repository, transaction_repository


class AppError(Exception):
    """Application error with a status code for API responses."""

    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class TransactionService:
    """Service layer for deposit/withdraw business rules and transaction records."""

    def __init__(self, account_repository_obj, transaction_repository_obj, db_connection_factory=get_db_connection):
        # receive repository objects from outside so this service is easy to test/mock
        self.account_repository = account_repository_obj
        self.transaction_repository = transaction_repository_obj
        # db factory is also injected so tests can use fake connections
        self.db_connection_factory = db_connection_factory

    def _parse_and_validate_account_id(self, account_id: int) -> int:
        """Allow only positive integer account IDs."""
        # account id should be a clean positive integer like 1, 2, 3...
        if not isinstance(account_id, int) or account_id <= 0:
            raise AppError("Account ID must be a positive integer.", 400)
        return account_id

    def _parse_and_validate_amount(self, amount: Any) -> Decimal:
        """Validate amount input and normalize it to two decimal places."""
        # convert via string so both numeric and string inputs are handled (ex: 25 or "25")
        try:
            numeric_amount = Decimal(str(amount))
        except (InvalidOperation, TypeError, ValueError):
            raise AppError("Amount must be a valid number.", 400)

        # business rule: deposit/withdraw amount must be more than zero
        if numeric_amount <= 0:
            raise AppError("Amount must be greater than zero.", 400)

        # keep the value at 2 decimals because money is saved as dollars/cents
        return numeric_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def deposit(self, account_id: int, amount: Any) -> dict:
        """Deposit money into an account and log a DEPOSIT transaction."""
        # step 1) validate request values early
        validated_account_id = self._parse_and_validate_account_id(account_id)
        validated_amount = self._parse_and_validate_amount(amount)

        # step 2) open db connection for transactional work
        connection = self.db_connection_factory()

        try:
            # step 3) start a db transaction
            connection.start_transaction()
            cursor = connection.cursor(dictionary=True)

            # Lock row to avoid race conditions when multiple requests hit same account.
            account = self.account_repository.find_by_id_for_update(cursor, validated_account_id)
            if not account:
                raise AppError("Account not found.", 404)

            # step 4) read current balance and compute new balance
            current_balance = Decimal(str(account["balance"]))
            updated_balance = current_balance + validated_amount

            # step 5) update account balance in accounts table
            self.account_repository.update_balance(cursor, validated_account_id, float(updated_balance))

            # step 6) add one transaction row so deposit is traceable later
            transaction = self.transaction_repository.create_transaction(
                cursor,
                validated_account_id,
                "DEPOSIT",
                float(validated_amount),
            )

            # step 7) commit both operations together
            connection.commit()

            # return a clean response object for controller/api layer
            return {
                "accountId": account["account_id"],
                "previousBalance": float(current_balance),
                "balance": float(updated_balance),
                "transaction": transaction,
            }
        except Exception:
            # if anything fails, undo partial updates
            connection.rollback()
            raise
        finally:
            # always close connection
            connection.close()

    def withdraw(self, account_id: int, amount: Any) -> dict:
        """Withdraw money from an account and log a WITHDRAW transaction."""
        # step 1) validate request values early
        validated_account_id = self._parse_and_validate_account_id(account_id)
        validated_amount = self._parse_and_validate_amount(amount)

        # step 2) open db connection for transactional work
        connection = self.db_connection_factory()

        try:
            # step 3) start a db transaction
            connection.start_transaction()
            cursor = connection.cursor(dictionary=True)

            # Lock row so the balance check and update stay atomic.
            account = self.account_repository.find_by_id_for_update(cursor, validated_account_id)
            if not account:
                raise AppError("Account not found.", 404)

            # step 4) parse current balance to decimal for precise math
            current_balance = Decimal(str(account["balance"]))

            # business rule: do not allow withdrawing more than available balance
            if validated_amount > current_balance:
                raise AppError(
                    "Insufficient balance. Cannot withdraw more than current balance.",
                    400,
                )

            # step 5) compute new balance after withdrawal
            updated_balance = current_balance - validated_amount

            # step 6) update account balance in accounts table
            self.account_repository.update_balance(cursor, validated_account_id, float(updated_balance))

            # step 7) add one transaction row for audit/history
            transaction = self.transaction_repository.create_transaction(
                cursor,
                validated_account_id,
                "WITHDRAW",
                float(validated_amount),
            )

            # step 8) commit both operations together
            connection.commit()

            # return a clean response object for controller/api layer
            return {
                "accountId": account["account_id"],
                "previousBalance": float(current_balance),
                "balance": float(updated_balance),
                "transaction": transaction,
            }
        except Exception:
            # if anything fails, undo partial updates
            connection.rollback()
            raise
        finally:
            # always close connection
            connection.close()

    def get_transactions(self, account_id: int) -> list[dict]:
        """Fetch account transaction history."""
        # validate id first before querying
        validated_account_id = self._parse_and_validate_account_id(account_id)
        connection = self.db_connection_factory()

        try:
            cursor = connection.cursor(dictionary=True)

            # ensure account exists before loading transactions
            account = self.account_repository.find_by_id(cursor, validated_account_id)
            if not account:
                raise AppError("Account not found.", 404)

            # fetch transactions from repository and shape response for api
            rows = self.transaction_repository.find_by_account_id(cursor, validated_account_id)
            return [
                {
                    "transactionId": row["txn_id"],
                    "type": row["txn_type"],
                    "amount": float(row["amount"]),
                    "date": row["created_at"],
                }
                for row in rows
            ]
        finally:
            connection.close()


# Default instance used by controllers so routes can call module-level functions.
transaction_service = TransactionService(account_repository, transaction_repository)


def deposit(account_id: int, amount: Any) -> dict:
    # thin wrapper so controllers can call transaction_service.deposit directly
    return transaction_service.deposit(account_id, amount)


def withdraw(account_id: int, amount: Any) -> dict:
    # thin wrapper so controllers can call transaction_service.withdraw directly
    return transaction_service.withdraw(account_id, amount)


def get_transactions(account_id: int) -> list[dict]:
    # thin wrapper so controllers can call transaction_service.get_transactions directly
    return transaction_service.get_transactions(account_id)

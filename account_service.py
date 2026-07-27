from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any

# responsible for retrieving and updating account data and saving transaction records
from python_backend.repositories import (
    account_repository,
    transaction_repository,
)


def validate_amount(amount: Any) -> Decimal:
    "Ensure the amount is numeric, positive, and rounded to two decimal places"

    # convert input into decimal
    # For example, both 12.5 and "12.5" can be handled correctly
    try:
        validated_amount = Decimal(str(amount))
    except (InvalidOperation, TypeError, ValueError):
        # raise an error when the amount cannot be converted into a number
        raise ValueError("Amount must be a valid number.")

    # deposits/withdrawals must always be greater than zero.
    if validated_amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    # round amount to two decimal places because money is normally
    # stored/displayed using dollars and cents.
    return validated_amount.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


def deposit(account_id: int, amount: Any):
    """Add money to an account and create a matching deposit transaction."""

    # validate/format the deposit amount before changing account data
    validated_amount = validate_amount(amount)

    # retrieve account using the provided account ID.
    account = account_repository.find_by_id(account_id)

    # stop the operation if the account does not exist.
    if account is None:
        raise ValueError("Account not found.")

    # convert stored balance into a decimal so the calculation
    # uses accurate monetary values
    current_balance = Decimal(str(account["balance"]))

    # add deposit amount to the account's current balance
    updated_balance = current_balance + validated_amount

    # save new balance using the account repository
    account_repository.update_balance(
        account_id,
        float(updated_balance),
    )

    # create a transaction record so the deposit appears
    # in the account's transaction history
    transaction = transaction_repository.create_transaction(
        account_id,
        "DEPOSIT",
        float(validated_amount),
    )

    # return transaction that was created
    return transaction


def withdraw(account_id: int, amount: Any):
    "Remove money from an account and create a matching withdrawal transaction"

    # validate/format the withdrawal amount before changing account data
    validated_amount = validate_amount(amount)

    # retrieve account using the provided account ID
    account = account_repository.find_by_id(account_id)

    # stop operation if the account does not exist
    if account is None:
        raise ValueError("Account not found.")

    # convert stored balance into a decimal for accurate calculations
    current_balance = Decimal(str(account["balance"]))

    # Prevent the user from withdrawing more money than the account contains
    if validated_amount > current_balance:
        raise ValueError(
            "Insufficient balance. Cannot withdraw more than the current balance."
        )

    # subtract withdrawal amount from the current balance
    updated_balance = current_balance - validated_amount

    # save updated balance using the account repository
    account_repository.update_balance(
        account_id,
        float(updated_balance),
    )

    # create transaction record so the withdrawal appears
    # in the account's transaction history.
    transaction = transaction_repository.create_transaction(
        account_id,
        "WITHDRAW",
        float(validated_amount),
    )

    # return transaction that was created
    return transaction
from models.transaction import Transaction


class TransactionRepository:
    def __init__(self):
        # Temporary hard-coded transaction data.
        self.transactions = []

    def save(self, transaction):
        # Assign next id for in-memory storage.
        if self.transactions:
            transaction.transaction_id = max(
                existing_transaction.transaction_id
                for existing_transaction in self.transactions
            ) + 1
        else:
            transaction.transaction_id = 1

        self.transactions.append(transaction)
        return transaction

    def get_by_id(self, transaction_id):
        for transaction in self.transactions:
            if transaction.transaction_id == transaction_id:
                return transaction
        return None

    def get_by_account_id(self, account_id):
        return [
            transaction
            for transaction in self.transactions
            if transaction.account_id == account_id
        ]

    def get_all(self):
        return self.transactions

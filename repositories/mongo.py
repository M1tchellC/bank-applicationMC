import os
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv
from pymongo import ASCENDING, MongoClient, ReturnDocument


## load in env mongodb username/password
load_dotenv(
    Path(__file__).resolve().parent.parent / "atlas-credentials.env"
)


@lru_cache(maxsize=1)
def get_database():
    # Read MongoDB connection settings from .env.
    mongodb_uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGODB_DB_NAME", "bank_application")

    if not mongodb_uri:
        raise ValueError("MONGODB_URI is not set. Add it to your .env file.")

    # Create one client/database object and reuse it.
    client = MongoClient(mongodb_uri)
    database = client[db_name]

    # Make sure required indexes exist before repositories use collections.
    _ensure_indexes(database)
    return database


def _ensure_indexes(database):
    # Allow collection names to be configured in .env.
    accounts_collection_name = os.getenv("MONGODB_ACCOUNTS_COLLECTION", "accounts")
    users_collection_name = os.getenv("MONGODB_USERS_COLLECTION", "users")
    transactions_collection_name = os.getenv("MONGODB_TRANSACTIONS_COLLECTION", "transactions")

    # Unique indexes keep our numeric IDs from duplicating.
    database[accounts_collection_name].create_index([("account_id", ASCENDING)], unique=True)
    database[users_collection_name].create_index([("user_id", ASCENDING)], unique=True)
    database[transactions_collection_name].create_index([("transaction_id", ASCENDING)], unique=True)

    # Query helper index for account transaction history lookups.
    database[transactions_collection_name].create_index([("account_id", ASCENDING), ("created_at", ASCENDING)])

    # Counter collection is used for auto-increment style numeric IDs.
    database.counters.create_index([("_id", ASCENDING)], unique=True)


def get_next_sequence(sequence_name: str) -> int:
    # Atomically increment and return the next numeric ID.
    counter = get_database().counters.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"value": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return int(counter["value"])

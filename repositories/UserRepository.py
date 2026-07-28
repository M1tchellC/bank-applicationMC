import os

from models.user import User
from repositories.mongo import get_database, get_next_sequence


class UserRepository:
    def __init__(self):
        # Connect to MongoDB and select the users collection.
        database = get_database()
        collection_name = os.getenv("MONGODB_USERS_COLLECTION", "users")
        self.users = database[collection_name]

    def save(self, user):
        # Assign a new numeric ID when creating a user.
        if user.user_id is None:
            user.user_id = get_next_sequence("user_id")

        # Store model fields in MongoDB.
        self.users.insert_one(
            {
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "created_at": user.created_at,
            }
        )
        return user

    def get_by_id(self, user_id):
        # Find one user by business user_id.
        document = self.users.find_one({"user_id": user_id})
        if document is None:
            return None

        # Convert MongoDB document back into User model.
        return User(
            user_id=document["user_id"],
            name=document["name"],
            email=document["email"],
            created_at=document.get("created_at"),
        )

    def get_all(self):
        # Return users sorted by numeric ID.
        documents = self.users.find().sort("user_id", 1)
        return [
            User(
                user_id=document["user_id"],
                name=document["name"],
                email=document["email"],
                created_at=document.get("created_at"),
            )
            for document in documents
        ]

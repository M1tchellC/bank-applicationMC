from models.user import User


class UserRepository:
    def __init__(self):
        # Temporary hard-coded data
        self.users = [
            User(
                name="Nate Levi",
                email="nate.levi@example.com",
                user_id=1,
            ),
            User(
                name="Naeem Saleem",
                email="naeem.saleem@example.com",
                user_id=2,
            ),
            User(
                name="Mitchell Carney",
                email="mitchell.carney@example.com",
                user_id=3,
            ),
        ]

    def save(self, user):
        # Find the largest existing ID, then add one
        if self.users:
            user.user_id = max(
                existing_user.user_id for existing_user in self.users
            ) + 1
        else:
            user.user_id = 1

        self.users.append(user)
        return user

    def get_by_id(self, user_id):
        # Get a user by their ID
        for user in self.users:
            if user.user_id == user_id:
                return user

        return None

    def get_all(self):
        # Return all users in the repository
        return self.users

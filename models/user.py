from datetime import datetime


class User:
    def __init__(self, name, email, user_id=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.created_at = datetime.now()
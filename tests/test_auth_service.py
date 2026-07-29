import os
import unittest
from unittest.mock import patch

from services.auth_service import AuthenticationError, AuthService


class FakeUserRepository:
    def __init__(self):
        self.users = []

    def save(self, user):
        user.user_id = len(self.users) + 1
        self.users.append(user)
        return user

    def get_by_email(self, email):
        return next((user for user in self.users if user.email == email), None)

    def get_by_id(self, user_id):
        return next((user for user in self.users if user.user_id == user_id), None)


class AuthServiceTests(unittest.TestCase):
    def setUp(self):
        self.repository = FakeUserRepository()
        self.service = AuthService(self.repository)
        self.settings = patch.dict(
            os.environ,
            {
                "JWT_SECRET_KEY": "test-only-secret-that-is-at-least-32-characters",
                "JWT_ALGORITHM": "HS256",
                "JWT_ISSUER": "bank-application",
                "JWT_AUDIENCE": "bank-application-api",
                "JWT_ACCESS_TOKEN_MINUTES": "15",
            },
        )
        self.settings.start()

    def tearDown(self):
        self.settings.stop()

    def test_register_hashes_password_and_normalizes_email(self):
        user = self.service.register(
            " Test User ", " Test@Example.com ", "correct-horse-battery"
        )

        self.assertEqual(user.name, "Test User")
        self.assertEqual(user.email, "test@example.com")
        self.assertNotEqual(user.password_hash, "correct-horse-battery")
        self.assertTrue(
            self.service.password_hash.verify(
                "correct-horse-battery", user.password_hash
            )
        )

    def test_login_and_token_round_trip(self):
        user = self.service.register(
            "Test User", "test@example.com", "correct-horse-battery"
        )
        authenticated = self.service.authenticate(
            "TEST@example.com", "correct-horse-battery"
        )
        token = self.service.create_access_token(authenticated)

        self.assertEqual(self.service.get_user_from_token(token).user_id, user.user_id)

    def test_incorrect_password_is_rejected(self):
        self.service.register(
            "Test User", "test@example.com", "correct-horse-battery"
        )

        with self.assertRaises(AuthenticationError):
            self.service.authenticate("test@example.com", "wrong-password")

    def test_duplicate_email_is_rejected(self):
        self.service.register(
            "First", "test@example.com", "correct-horse-battery"
        )

        with self.assertRaisesRegex(ValueError, "already registered"):
            self.service.register(
                "Second", "TEST@example.com", "another-long-password"
            )

    def test_tampered_token_is_rejected(self):
        user = self.service.register(
            "Test User", "test@example.com", "correct-horse-battery"
        )
        token = self.service.create_access_token(user)
        tampered_token = token[:-1] + ("a" if token[-1] != "a" else "b")

        with self.assertRaises(AuthenticationError):
            self.service.get_user_from_token(tampered_token)


if __name__ == "__main__":
    unittest.main()

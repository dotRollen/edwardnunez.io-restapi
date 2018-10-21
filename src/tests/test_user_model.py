import unittest
import time
from datetime import datetime
from backend.app import create_app, db
from backend.app.models.auth import User, AnonymousUser, Role, Permission


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        Role.insert_roles()

    def tearDown(self):
        try:
            db.connection.drop_database('test')
        except Exception:
            db.connection.client.drop_database('test')
        self.app_context.pop()

    def test_password_setter(self):
        u = User()
        u.password = "cat"
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User()
        u.password = "cat"
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User()
        u.password = "cat"
        self.assertTrue(u.verify_password("cat"))
        self.assertFalse(u.verify_password("dog"))

    def test_password_salts_are_random(self):
        u = User()
        u.password = "cat"
        u2 = User()
        u2.password = "cat"
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_valid_confirmation_token(self):
        u = User()
        u.save()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        u1 = User(email="john@example.com", username="john")
        u1.password = "cat"
        u2 = User(email="susan@example.org", username="susan")
        u2.password = "cat"
        u1.save()
        u2.save()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        u = User()
        u.password = "cat"
        u.save()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm(token))

    def test_valid_reset_token(self):
        u = User()
        u.password = "cat"
        u.save()
        token = u.generate_reset_token()
        new_password = "testvalidreset"
        self.assertTrue(u.reset_password(token, new_password))
        u = User.objects(id=u.id).first()
        self.assertTrue(u.verify_password(new_password))

    def test_invalid_reset_token(self):
        u = User()
        u.password = "cat"
        u.save()
        token = u.generate_reset_token()
        self.assertFalse(u.reset_password(token + "a", "horse"))
        self.assertTrue(u.verify_password("cat"))

    def test_valid_email_change_token(self):
        u = User(email="john@example.com")
        u.password = "cat"
        u.save()
        token = u.generate_email_change_token("susan@example.org")
        self.assertTrue(u.change_email(token))
        self.assertTrue(u.email == "susan@example.org")

    def test_invalid_email_change_token(self):
        u1 = User(email="john@example.com", username="john")
        u1.password = "cat"
        u1.save()
        u2 = User(email="susan@example.org", username="susan")
        u2.password = "dog"
        u2.save()
        token = u1.generate_email_change_token("david@example.net")
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == "susan@example.org")

    def test_duplicate_email_change_token(self):
        u1 = User(email="john@example.com", username="john")
        u1.password = 'cat'
        u2 = User(email="susan@example.org", username="susan")
        u2.password = 'dog'
        u1.save()
        u2.save()
        token = u2.generate_email_change_token("john@example.com")
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == "susan@example.org")

    def test_user_role(self):
        u = User(email="john@example.com")
        u.password = "cat"
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_moderator_role(self):
        r = Role.objects(name="Moderator").first()
        u = User(email="john@example.com", role=r)
        u.password = "cat"
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertTrue(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_administrator_role(self):
        r = Role.objects(name="Administrator").first()
        u = User(email="john@example.com", role=r)
        u.password = "cat"
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertTrue(u.can(Permission.MODERATE))
        self.assertTrue(u.can(Permission.ADMIN))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))
        self.assertFalse(u.can(Permission.COMMENT))
        self.assertFalse(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_timestamps(self):
        u = User()
        u.password = 'cat'
        u.save()
        self.assertTrue((datetime.utcnow() - u.member_since).total_seconds() < 3)
        self.assertTrue((datetime.utcnow() - u.last_seen).total_seconds() < 3)

    def test_ping(self):
        u = User()
        u.password = 'cat'
        u.save()
        time.sleep(2)
        last_seen_before = u.last_seen
        u.ping()
        self.assertTrue(u.last_seen > last_seen_before)

    def test_to_json(self):
        u = User(email="john@example.com")
        u.password = "cat"
        u.save()
        with self.app.test_request_context("/"):
            json_user = u.to_json()
        expected_keys = [
            "url",
            "username",
            "member_since",
            "last_seen",
        ]
        self.assertEqual(sorted(json_user.keys()), sorted(expected_keys))
        self.assertEqual("/api/v1/users/" + str(u.id), json_user["url"])

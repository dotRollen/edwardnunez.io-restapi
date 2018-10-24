import unittest
from flask import current_app
from backend.app import create_app, db


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        try:
            db.connection.drop_database('test')
        except Exception:
            db.connection.client.drop_database('test')
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config["TESTING"])

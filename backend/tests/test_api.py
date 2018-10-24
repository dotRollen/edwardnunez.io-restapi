import unittest
import json
import re
from base64 import b64encode
from backend.app import create_app, db
from backend.app.models.auth import User, Role


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        Role.insert_roles()
        self.client = self.app.test_client()

    def tearDown(self):
        try:
            db.connection.drop_database('test')
        except Exception:
            db.connection.client.drop_database('test')
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_404(self):
        response = self.client.get(
            '/wrong/url',
            headers=self.get_api_headers('email', 'password'))
        self.assertEqual(response.status_code, 404)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['error'], 'not found')

    def test_no_auth(self):
        response = self.client.get('/api/v1/projects/',
                                   content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_bad_auth(self):
        # add a user
        r = Role.objects(name='User').first()
        self.assertIsNotNone(r)
        u = User(email='john@example.com',  confirmed=True,
                 role=r)
        u.password = 'cat'
        u.save()

        # authenticate with bad password
        response = self.client.get(
            '/api/v1/projects/',
            headers=self.get_api_headers('john@example.com', 'dog'))
        self.assertEqual(response.status_code, 401)

    def test_token_auth(self):
        # add a user
        r = Role.objects(name='User').first()
        self.assertIsNotNone(r)
        u = User(email='john@example.com', confirmed=True,
                 role=r)
        u.password = 'cat'
        u.save()

        # issue a request with a bad token
        response = self.client.get(
            '/api/v1/projects/',
            headers=self.get_api_headers('bad-token', ''))
        self.assertEqual(response.status_code, 401)

        # get a token
        response = self.client.post(
            '/api/v1/tokens/',
            headers=self.get_api_headers('john@example.com', 'cat'))

        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(json_response.get('token'))
        token = json_response['token']

        # issue a request with the token
        response = self.client.get(
            '/api/v1/projects/',
            headers=self.get_api_headers(token, ''))
        self.assertEqual(response.status_code, 200)

    def test_anonymous(self):
        response = self.client.get(
            '/api/v1/projects/',
            headers=self.get_api_headers('', ''))
        self.assertEqual(response.status_code, 401)

    def test_unconfirmed_account(self):
        # add an unconfirmed user
        r = Role.objects(name='User').first()
        self.assertIsNotNone(r)
        u = User(email='john@example.com', confirmed=False,
                 role=r)
        u.password = 'cat'
        u.save()

        # get list of posts with the unconfirmed account
        response = self.client.get(
            '/api/v1/projects/',
            headers=self.get_api_headers('john@example.com', 'cat'))
        self.assertEqual(response.status_code, 403)

    def test_users(self):
        # add two users
        r = Role.objects(name='User').first()
        self.assertIsNotNone(r)
        u1 = User(email='john@example.com', username='john',
                  confirmed=True, role=r)
        u1.password = 'cat'
        u2 = User(email='susan@example.com', username='susan',
                  confirmed=True, role=r)
        u2.password = 'dog'
        u1.save()
        u2.save()

        # get users
        response = self.client.get(
            '/api/v1/users/{}'.format(u1.id),
            headers=self.get_api_headers('susan@example.com', 'dog'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['username'], 'john')
        response = self.client.get(
            '/api/v1/users/{}'.format(u2.id),
            headers=self.get_api_headers('susan@example.com', 'dog'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['username'], 'susan')

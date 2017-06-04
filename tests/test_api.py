import json

from expert_tourist.models import User
from tests.tests import BaseTestConfig


class TestAPI(BaseTestConfig):
    random_user = {
        'email': 'shameless-driver2022@live.cr',
        'password': 'tmslaegolbin//tm'
    }

    def test_sign_up(self):
        self.assertIsNone(User.query.filter_by(email=self.random_user['email']).first())

        res = self.app.post(
            "/api/sign_up",
            data=json.dumps(self.random_user),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(json.loads(res.data.decode("utf-8"))["token"])
        self.assertEqual(
            User.query.filter_by(email=self.random_user["email"]).first().email,
            self.random_user["email"]
        )

    def test_user_validate_credentials(self):
        user = User(**self.random_user).create()
        self.assertIsNotNone(user)
        self.assertIsNotNone(self.random_user['email'], self.random_user['password'])

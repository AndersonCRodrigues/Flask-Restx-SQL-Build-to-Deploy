import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.users import UserModel


class UserTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config=config_dict["test"])

        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()

    def tearDown(self):
        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None

    def test_user_registration(self):

        data = {
            "username": "testuser",
            "email": "test@email.com",
            "password": "password",
        }

        response = self.client.post("/auth/signup", json=data)

        user = UserModel.query.filter_by(email="test@email.com").first()

        assert response.status_code == 201
        assert user.username == "testuser"

    def test_login(self):
        data = {
            "email": "test@email.com",
            "password": "password",
        }

        response = self.client.post("/auth/login", json=data)

        assert response.status_code == 404

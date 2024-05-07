import unittest
from flask_jwt_extended import create_access_token
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.orders import OrderModel


class OrderTestcase(unittest.TestCase):
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

    def test_get_all_orders(self):
        token = create_access_token(identity="testuser")

        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get("/orders/", headers=headers)

        assert response.status_code == 200

        assert response.json == []

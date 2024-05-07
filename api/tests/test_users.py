import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db


class UserTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config=config_dict["testing"])

        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()

    def tearDown(self):
        pass

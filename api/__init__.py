from flask import Flask
from flask_restx import Api
from .order.views import order_namespace
from .auth.view import auth_namespace
from .config.config import config_dict
from .utils import db
from .models.orders import OrderModel
from .models.users import UserModel
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from werkzeug.exceptions import NotFound, MethodNotAllowed


def create_app(config=config_dict["dev"]):
    app = Flask(__name__)

    app.config.from_object(config)

    api = Api(app)

    api.add_namespace(order_namespace)
    api.add_namespace(auth_namespace, path="/auth")

    db.init_app(app)

    Migrate(app, db)

    JWTManager(app)

    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not Found"}, 404

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method Not Allowed"}, 405

    @app.shell_context_processor
    def make_shell_context():
        return {"db": db, "User": UserModel, "Order": OrderModel}

    return app

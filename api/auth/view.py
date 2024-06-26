from http import HTTPStatus
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.users import UserModel
from werkzeug.exceptions import (
    Conflict,
    NotFound,
    Unauthorized,
)


auth_namespace = Namespace("auth", description="Namespace for authentication")

signup_model = auth_namespace.model(
    "SignUp",
    {
        "username": fields.String(required=True, description="A usernme"),
        "email": fields.String(required=True, description="An email"),
        "password": fields.String(required=True, description="A password"),
    },
)

user_model = auth_namespace.model(
    "User",
    {
        "id": fields.Integer(),
        "username": fields.String(required=True, description="A usernme"),
        "email": fields.String(required=True, description="An email"),
        "is_active": fields.Boolean(
            description="This show that User is active",
        ),
        "is_staff": fields.Boolean(description="This show that User is staff"),
    },
)

login_model = auth_namespace.model(
    "Login",
    {
        "email": fields.String(required=True, description="An email"),
        "password": fields.String(required=True, description="a passwpord"),
    },
)


@auth_namespace.route("/signup")
class SignUp(Resource):

    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """
        Create a new user account
        """

        data = request.get_json()

        try:

            new_user = UserModel(
                username=data.get("username"),
                email=data.get("email"),
                password_hash=generate_password_hash(data.get("password")),
            )

            new_user.save()

            return new_user, HTTPStatus.CREATED

        except Exception as e:
            raise Conflict(
                f"User with email {data.get('email')} exists!",
            ) from e


@auth_namespace.route("/login")
class Login(Resource):

    @auth_namespace.expect(login_model)
    def post(self):
        """
        Generate a JWT pair
        """

        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        user = UserModel.query.filter_by(email=email).first()

        if user is None:
            raise NotFound("User not found")

        if not check_password_hash(user.password_hash, password):
            raise Unauthorized("Invalid password")

        access_token = create_access_token(user.username)
        refresh_token = create_refresh_token(user.username)

        response = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        return response, HTTPStatus.OK


@auth_namespace.route("/refresh")
class Refresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        """
        Generete a new access token
        """
        username = get_jwt_identity()

        access_token = create_access_token(identity=username)

        return {"access_token": access_token}, HTTPStatus.OK

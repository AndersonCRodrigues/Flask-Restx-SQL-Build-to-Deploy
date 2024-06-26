from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields

from api.models.users import UserModel
from ..models.orders import OrderModel
from ..utils import db


order_namespace = Namespace("orders", description="Namespace for order")

order_model = order_namespace.model(
    "Order",
    {
        "id": fields.Integer(description="An ID"),
        "size": fields.String(
            description="Size of order",
            required=True,
            enum=["SMALL", "MEDIUM", "LARGE", "EXTRA_LARGE"],
        ),
        "order_status": fields.String(
            description="The status of the Order",
            required=True,
            enum=["PENDING", "IN_TRANSIT", "DELIVERED"],
        ),
        "flavour": fields.String(
            description="Flavour of order",
        ),
    },
)

order_status_model = order_namespace.model(
    "OrderStatus",
    {
        "order_status": fields.String(
            required=True,
            description="Order status",
            enum=["PENDING", "IN_TRANSIT", "DELIVERED"],
        )
    },
)


@order_namespace.route("/")
class OrderGetCreate(Resource):

    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(description="Retriver all orders")
    @jwt_required()
    def get(self):
        """
        Get all Orders
        """
        return OrderModel.query.all(), HTTPStatus.OK

    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def post(self):
        """
        Place a new order
        """

        username = get_jwt_identity()

        current_user = UserModel.query.filter_by(username=username).first()

        data = order_namespace.payload

        new_order = OrderModel(
            size=data["size"],
            quantity=data["quantity"],
            flavour=data["flavour"],
        )

        new_order.customer = current_user.id

        new_order.save()

        return new_order, HTTPStatus.CREATED


@order_namespace.route("/<int:order_id>/")
class GetUpdateDelete(Resource):

    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description="Retrive an order by ID",
        params={
            "order_id": "An ID for given a order",
        },
    )
    @jwt_required()
    def get(self, order_id):
        """
        Retrive an order by id
        """
        return OrderModel.get_by_id(order_id), HTTPStatus.OK

    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def put(self, order_id):
        """
        Update an order with id
        """
        order_to_update = OrderModel.get_by_id(order_id)

        data = order_namespace.payload

        order_to_update.quantity = data["quantity"]
        order_to_update.size = data["size"]
        order_to_update.flavour = data["flavour"]

        db.session.commit()

        return order_to_update, HTTPStatus.OK

    @jwt_required()
    def delete(self, order_id):
        """
        Delete an order with id
        """
        if order_to_delete := OrderModel.get_by_id(order_id):
            order_to_delete.delete()

            return (
                {"message": f"Order with id {order_id} has been deleted"},
                HTTPStatus.OK,
            )

        return ({"mesage": "Order not found"}, HTTPStatus.NOT_FOUND)


@order_namespace.route("/user/<int:user_id>/order/<int:order_id>/")
class GetSpecificOrderByUser(Resource):

    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self, user_id, order_id):
        """
        Get a user's specific order
        """

        if current_user := UserModel.query.filter_by(id=user_id).first():
            if order := OrderModel.query.filter_by(
                id=order_id, customer=current_user.id
            ).first():
                return order, HTTPStatus.OK
            else:
                return {"message": "Order not found"}, HTTPStatus.NOT_FOUND
        else:
            return {"message": "User not found"}, HTTPStatus.NOT_FOUND


@order_namespace.route("/user/<int:user_id>/")
class UserOrders(Resource):

    @order_namespace.marshal_list_with(order_model)
    @jwt_required()
    def get(self, user_id):
        """
        Get all orders by a specific user
        """
        user = UserModel.get_by_id(user_id)

        return user.orders, HTTPStatus.OK


@order_namespace.route("/status/<int:order_id>/")
class UpdateOrderStatus(Resource):

    @order_namespace.expect(order_status_model)
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def patch(self, order_id):
        """
        Update an order's status
        """

        data = order_namespace.payload

        order_to_update = OrderModel.get_by_id(order_id)

        order_to_update.order_status = data["order_status"]

        db.session.commit()

        return order_to_update, HTTPStatus.OK

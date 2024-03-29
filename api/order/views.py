from http import HTTPStatus
from flask_restx import Namespace, Resource, fields
from ..models.orders import OrderModel


order_namespace = Namespace("orders", description="Namespace for order")

order_model = order_namespace.model(
    "Order",
    {
        "id": fields.Integer(description="An ID"),
        "size": fields.String(
            description="Size of order",
            required=True,
            enum=["SMAL", "MEDIUM", "LARGE", "EXTRA_LARGE"],
        ),
        "order_status": fields.String(
            description="The status of the Order",
            required=True,
            enum=["PENDING" "IN_TRANSIT", "DELIVERED"],
        ),
    },
)


@order_namespace.route("/")
class OrderGetCreate(Resource):

    @order_namespace.marshal_with(order_model)
    def get(self):
        """
        Get all Orders
        """
        return OrderModel.query.all(), HTTPStatus.OK

    def post(self):
        """
        Place a new order
        """
        pass


@order_namespace.route("/<int:order_id>/")
class GetUpdateDelete(Resource):

    def get(self, order_id):
        """
        Retrive an order by id
        """
        pass

    def put(self, order_id):
        """
        Update an order with id
        """
        pass

    def delete(self, order_id):
        """
        Delete an order with id
        """
        pass


@order_namespace.route("/user/<int:user_id>/order/<int:order_id>/")
class GetSpecificOrderByUser(Resource):

    def get(self, user_id, order_id):
        """
        Get a user's specific order
        """
        pass


@order_namespace.route("/user/<int:user_id>/orders/")
class UserOrders(Resource):

    def get(self, user_id):
        """
        Get all orders by a specific
        """
        pass


@order_namespace.route("/status/<int:order_id>/")
class UpdateOrderStatus(Resource):

    def patch(self, order_id):
        """
        Update an order's status
        """
        pass

from enum import Enum
from ..utils import db
from datetime import datetime


class Sizes(Enum):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    EXTRA_LARGE = 'extra_large'


class OrderStatus(Enum):
    PENDING = 'pending'
    IN_TRANSIT = 'in-transit'
    DELIVERED = 'delivered'


class OrderModel(db.Model):

    __tablename__ = 'orders'
    id = db.Column(db.Integer(), primary_key=True)
    size = db.Column(db.Enum(Sizes), default=Sizes.SMALL)
    order_status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING)
    flavour = db.Column(db.String(), nullable=False)
    quantity = db.Column(db.Integer())
    date_created = db.Column(db.DateTime(), default=datetime.now)
    customer = db.Column(db.Integer(), db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<Order {self.id}>"

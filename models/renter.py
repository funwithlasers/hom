"""Database models."""
from .. import db
import datetime
from .lease import Lease
from .property import Property


class Renter(db.Model):
    """ Model for user renters """

    __tablename__ = "renters"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    first_name = db.Column(
        db.String(50),
        nullable=False
    )
    last_name = db.Column(
        db.String(50),
        nullable=False
    )
    email = db.Column(
        db.String(200),
        nullable=False
    )
    phone = db.Column(
        db.String(200),
        nullable=False
    )
    created_on = db.Column(
        db.DateTime, 
        default=datetime.datetime.utcnow
    )
    """Foreign Keys"""
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey("users.id")
    )

    """Helper Functions"""
    def most_recent_lease(self):
        return Lease.query.filter_by(renter_id=self.id).order_by('start_date').first()

    def current_lease(self):
        if not self.most_recent_lease() or datetime.datetime.utcnow() > self.most_recent_lease().end_date:
            return None
        return self.most_recent_lease()

    def current_address(self):
        if not self.current_lease():
            return None
        return Property.query.filter_by(id = self.current_lease().property_id).first()

    """ SQLAlchemy relationships """
    payments = db.relationship("Payment", backref="renter")

    def __repr__(self):
        return '<Renter {}>'.format(self.first_name)

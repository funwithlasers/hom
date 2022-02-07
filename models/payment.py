"""Database models."""
from .. import db
import datetime


class Payment(db.Model):
    """Model for user payments"""
     
    __tablename__ = "payments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    description = db.Column(
        db.String(200),
        nullable=True
    )
    user_id = db.Column(    # person getting paid
        db.Integer, 
        db.ForeignKey("users.id"),
        nullable=False
    )
    renter_id = db.Column(  # person making the payment
        db.Integer, 
        db.ForeignKey("renters.id"),
        nullable=False
    )
    date = db.Column(
        db.DateTime,
        nullable=True
    )
    amount = db.Column(
        db.Float,
        nullable=False
    )
    lease_id = db.Column(
        db.Integer, 
        db.ForeignKey("leases.id"),
        nullable=True   #   [OPTIONAL FIELD] non-lease payments also available (deposit)
    )
    created_on = db.Column(
        db.DateTime, 
        default=datetime.datetime.utcnow
    )

    def __repr__(self):
        return '<Payment -- date: {}, amount: {}>'.format(self.date, self.amount)


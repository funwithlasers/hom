"""Database models."""
from .. import db
import datetime


class Address(db.Model):
    """Model for addresses"""

    __tablename__ = "addresses"


    id = db.Column(
        db.Integer,
        primary_key=True
    )
    street = db.Column(
        db.String(200),
        nullable=False
    )
    city = db.Column(
        db.String(40),
        nullable=False
    )
    state = db.Column(
        db.String(40),
        nullable=False
    )
    zip = db.Column(
        db.Integer,
        nullable=False
    )
    created_on = db.Column(
        db.DateTime, 
        default=datetime.datetime.utcnow
    )

    """SQLAlchemy Relationships"""
    property = db.relationship("Property", backref=("address"), uselist = False) #   one-to-one


    def __repr__(self):
        return '<Address {}>'.format(self.street)
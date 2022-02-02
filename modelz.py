"""Database models."""
from . import db
import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """Model for user accounts."""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    first_name = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )
    last_name = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )
    email = db.Column(
        db.String(200),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
    )
    created_on = db.Column(
        db.DateTime, 
        default=datetime.datetime.utcnow
    )
    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    """ SQLAlchemy relationships """
    properties = db.relationship("Property", backref="user")

    """ Helper functions """
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.last_name,',',self.first_name)



class Address(db.Model):
    """ Model for addresses """

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

    """ SQLAlchemy Relationships """
    property = db.relationship("Property", backref=("address"), uselist = False) #   one-to-one


    def __repr__(self):
        return '<Address {}>'.format(self.street)



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
        unique=True,
        nullable=False
    )
    phone = db.Column(
        db.String(200),
        unique=True,
        nullable=False
    )
    created_on = db.Column(
        db.DateTime, 
        default=datetime.datetime.utcnow
    )
    """Foreign Keys"""
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    """Helper Functions"""
    def most_recent_lease(self):
        return Lease.query.filter_by(renter_id=self.id).order_by('start_date').first()

    def current_lease(self):
        if not self.most_recent_lease() or datetime.datetime.utcnow() > self.most_recent_lease().end_date:
            return None
        return self.most_recent_lease()

    """ SQLAlchemy relationships """
    payments = db.relationship("Payment", backref="renter")

    def __repr__(self):
        return '<Renter {}>'.format(self.first_name)


class Lease(db.Model):
    """ Model for user leases """

    __tablename__ = "leases"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    start_date = db.Column(
        db.DateTime,
        nullable=False
    )
    end_date = db.Column(
        db.DateTime
    )
    rate = db.Column(db.Float)
    terms = db.Column(
        db.Integer,
        nullable=False,
        default = 12
    )
    property_id = db.Column(db.Integer, db.ForeignKey("properties.id"))
    renter_id = db.Column(db.Integer, db.ForeignKey("renters.id"))
    created_on = db.Column(
        db.DateTime, 
        default=datetime.datetime.utcnow
    )

    """ SQLAlchemy relationships """
    payments = db.relationship("Payment", backref="lease")
    renter = db.relationship("Renter", backref="leases")

    def __repr__(self):
        return '<Lease {} - {}>'.format(self.start_date.month + self.start_date.month, self.end_date.month + self.start_date.year)


class Payment(db.Model):
    """ Model for user payments """
     
    __tablename__ = "payments"

    id = db.Column(
        db.Integer,
        primary_key=True
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


class Property(db.Model):
    """Model for properties."""

    __tablename__ = "properties"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"))
    # TODO: put image of property here
    # TODO: consider adding cost to owner. enabled profit, etc.
    created_on = db.Column(
        db.DateTime, 
        default=datetime.datetime.utcnow
    )

    """SQLAlchemy relationships"""
    leases = db.relationship("Lease", backref="property")

    """ Helper Funtions """
    def most_recent_lease(self):
        return Lease.query.filter_by(property_id=self.id).order_by('start_date').first()

    def current_lease(self):
        if not self.most_recent_lease() or datetime.datetime.utcnow() > self.most_recent_lease().end_date:
            return None
        return self.most_recent_lease()

    def __repr__(self):
        return '<{}>'.format(self.address.street)
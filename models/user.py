"""Database models."""
from .. import db
import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """Model for user accounts."""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key = True
    )
    username - db.Column(
        db.String(15),
        unique = True,
        nullable = False
    )
    first_name = db.Column(
        db.String(50),
        unique = True,
        nullable = False
    )
    last_name = db.Column(
        db.String(50),
        unique = True,
        nullable = False
    )
    email = db.Column(
        db.String(200),
        unique = True,
        nullable = False
    )
    password = db.Column(
        db.String(200),
        nullable = False
    )
    created_on = db.Column(
        db.DateTime, 
        default = datetime.datetime.utcnow
    )
    last_login = db.Column(
        db.DateTime,
        index = False,
        unique = False,
        nullable = True
    )

    """ SQLAlchemy relationships """
    # Samle below
    # properties = db.relationship("Property", backref="user")

    """ Helper functions """
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


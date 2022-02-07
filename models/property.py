from .. import db
import datetime
from .lease import Lease

class Property(db.Model):
    """Model for properties."""

    __tablename__ = "properties"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    image = db.Column(
        db.LargeBinary,
        nullable = True
    )
    created_on = db.Column(
        db.DateTime, 
        default=datetime.datetime.utcnow
    )
    """Foreign Keys"""
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"))
    # TODO: put image of property here
    # TODO: consider adding cost to owner. enabled profit, etc.


    """SQLAlchemy relationships"""
    leases = db.relationship("Lease", backref="property")

    """Helper Funtions"""
    def most_recent_lease(self):
        return Lease.query.filter_by(property_id=self.id).order_by('start_date').first()

    def current_lease(self):
        if not self.most_recent_lease() or datetime.datetime.utcnow() > self.most_recent_lease().end_date:
            return None
        return self.most_recent_lease()

    def __repr__(self):
        return '<{}>'.format(self.address.street)
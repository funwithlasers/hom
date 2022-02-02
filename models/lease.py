"""Database models."""
from .. import db
import datetime
from .payment import Payment
# from dateutil.relativedelta import relativedelta
from flask_login import current_user


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

    """Helper funtions
    def gen_lease_payments(self):
        date = self.start_date
        if date.day != 1:
            #add a prorate thing
            date.day = 1
            date = date + relativedelta(months=1)
        for p in range(self.terms):
            payment = Payment(
                user_id = current_user.id
                renter_id = self.renter_id
                date = # TODO: this
                amount = 0
                lease_id = self.id
            )
            db.session.add(payment)
            db.session.commit()
"""

    """ SQLAlchemy relationships """
    payments = db.relationship("Payment", backref="lease")
    renter = db.relationship("Renter", backref="leases")

    def __repr__(self):
        return '<Lease {} - {}>'.format(self.start_date.month + self.start_date.month, self.end_date.month + self.start_date.year)


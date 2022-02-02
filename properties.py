"""Routes for user authentication."""
from flask import redirect, render_template, flash, Blueprint, request, url_for
from flask_login import current_user
from flask import current_app
from .forms import LoginForm, SignupForm, PropertyForm, RenterForm, LeaseForm, PaymentForm
# from .models import db, Property, Address, Renter, User, Lease, Payment
from . import db
from .models.address import Address
from .models.lease import Lease
from .models.payment import Payment
from .models.property import Property
from .models.renter import Renter
from .models.user import User
from .auth import auth_bp
import binascii


# Blueprint Configuration
property_bp = Blueprint(
    'property_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@property_bp.route('/add_property', methods=['GET', 'POST'])
def add_property():
    """
    Registration form to create new property  accounts.
    GET: Serve registration page.
    POST: Validate form, create new property , redirect user to profile.
    """
    form = PropertyForm()

    if form.validate_on_submit():
        if current_user.is_authenticated:
            """
            I have chosen to not require uniqueness for addresses to prevent users blocking addresses and confidentiality
            TODO: require unique per user
            """
            image = None

            address = Address(
                street = form.street.data,
                city = form.city.data,
                state = form.state.data,
                zip = form.zip.data,
            )
            db.session.add(address)
            db.session.commit()

            if form.image.data:
                image = convert_to_binary_data(form.image.data)

            property_ = Property(
                user_id = current_user.id,
                address_id = address.id,
                image = image
            )
            db.session.add(property_)
            db.session.commit()
            return redirect(url_for('property_bp.properties'))
        flash("U MUST BE LOGGED IN TO SEE THIS Pge")
        return redirect(url_for('auth_bp.login'))   # Send to login page if not logged in
    return render_template(
            'add_property.jinja2',
            title = 'Add a property',
            form = form,
            # template = 'coral', # this sets the class of the main html <body> tag
            body = "template body delete this"
        )


@property_bp.route('/properties', methods=['GET', 'POST'])
def properties():
    """
    Display Property Properties
    GET: Serve registration page.
    POST: Validate form, create new property property, redirect user to profile.
    """        
    if current_user.is_authenticated:
        results = Property.query.join(Address, Property.address_id == Address.id) \
                                .outerjoin(Lease, Property.id == Lease.property_id) \
                                .outerjoin(Renter, Lease.renter_id == Renter.id) \
                                .filter(Property.user_id == current_user.id).all()

        return render_template(
                'properties.jinja2',
                title = 'Your property properties',
                results = results
            )
    flash("U MUST BE LOGGED IN TO SEE THIS Pge")
    return redirect(url_for('auth_bp.login'))



@property_bp.route('/property/<property_id>', methods=['GET', 'POST'])
def view_property(property_id):
    if current_user.is_authenticated:
        property_ = Property.query.filter_by(id=property_id).first()
        lease = property_.current_lease()
        return render_template(
            'view_property.jinja2',
            title = property_.address,
            template = 'properties-page',
            property = property_,
            current_lease = lease
        )
    return redirect(url_for('auth_bp.login'))


@property_bp.route('/add_renter', methods=['GET', 'POST'])
def add_renter():
    """
    Registration form to create new renter.
    GET: Serve registration page.
    POST: Validate form, create new renter, redirect user to profile.
    """

    if not current_user.is_authenticated:
        flash("U MUST BE LOGGED IN TO SEE THIS Pge")
        return redirect(url_for('auth_bp.login'))   # Send to login page if not logged in

    renter_form = RenterForm()
    if renter_form.validate_on_submit(): 
            """
            I have chosen to not require uniqueness for any of these fields to prevent users blocking addresses
            TODO: require unique per user (email, phone number)
            """
            renter = Renter(
                first_name = renter_form.first_name.data,
                last_name = renter_form.last_name.data,
                email = renter_form.email.data,
                phone = renter_form.phone.data,
                user_id = current_user.id
            )
            db.session.add(renter)
            db.session.commit()
           
            return redirect(url_for('main_bp.dashboard'))
       
    return render_template(
            'add_renter.jinja2',
            title = 'Add a renter',
            renter_form = renter_form,
            # template = 'signup-page', # Some css thing to clean up
            body = "renter body @properties.py",
        )



@property_bp.route('/property/<property_id>/lease', methods=['GET', 'POST'])
def add_lease(property_id):
    """
    Registration form to create new lease.
    GET: Serve registration page.
    POST: Validate form, create new lease
    """
    if current_user.is_authenticated:
        property_ = Property.query.filter(Property.id == property_id).first()
        if property_.user_id == current_user.id:
            form = LeaseForm()
            form.renter.choices = [(r.id, r.first_name) for r in Renter.query.filter(Renter.user_id == current_user.id).all()]

            if form.validate_on_submit():
                """
                I have chosen to not require uniqueness for any of these fields to prevent users blocking addresses
                TODO: require unique per user (email, phone number)
                """
                lease = Lease(
                    start_date = form.start_date.data,
                    end_date = form.end_date.data,
                    rate = form.rate.data,
                    terms = form.terms.data,
                    renter_id = form.renter.data,
                    property_id = property_id
                )
                db.session.add(lease)
                db.session.commit()
                return redirect(url_for('property_bp.view_property', property_id = property_id))
            return render_template(
                'lease.jinja2',
                title = 'Add a lease',
                form = form,
                # template = 'signup-page', # Some css thing to clean up
                body = "lease body @properties.py",
            )
            flash("You do not have access to this page")
        return redirect(url_for('property_bp.renters'))
    flash("U MUST BE LOGGED IN TO SEE THIS Pge")
    return redirect(url_for('auth_bp.login'))   # Send to login page if not logged in
    


@property_bp.route('/renters', methods=['GET', 'POST'])
def renters():
    """
    Display Renter Properties
    GET: Serve renters page.
    POST: Validate form, create new renter property, redirect user to profile.
    """        
    if current_user.is_authenticated:

        # TODO: Fix this query it sucks
        renters = Renter.query.outerjoin(Lease, Renter.id == Lease.renter_id) \
                                .outerjoin(Payment, Lease.id == Payment.lease_id) \
                                .outerjoin(Property, Lease.property_id == Property.id) \
                                .filter(Renter.user_id == current_user.id).all()

        return render_template(
                'renters.jinja2',
                title = 'Your renters',
                body = "Your renters",
                name_order_first_last = True,   #TODO: implement toggle (js button or setting)
                renters = renters,
                properties = properties
            )
    flash("U MUST BE LOGGED IN TO SEE THIS Pge")
    return redirect(url_for('auth_bp.login'))


@property_bp.route('/renter/<renter_id>', methods=['GET', 'POST'])
def renter(renter_id):
    if current_user.is_authenticated:
        renter = Renter.query.outerjoin(Lease, Renter.id == Lease.renter_id) \
                                .outerjoin(Payment, Lease.id == Payment.lease_id) \
                                .outerjoin(Property, Lease.property_id == Property.id) \
                                .filter(Renter.id == renter_id).first()
        return render_template(
            'view_renter.jinja2',
            # template = '',
            renter = renter
        )
    return redirect(url_for('auth_bp.login'))


@property_bp.route('/renter/<renter_id>/add_payment', methods=['GET', 'POST'])
def add_payment(renter_id):
    if current_user.is_authenticated:
        renter = Renter.query.filter(Renter.id == renter_id).first()
        if renter.user_id == current_user.id:
            form = PaymentForm()
            if form.validate_on_submit():
                payment = Payment(
                    date = form.date.data,
                    amount = form.amount.data,
                    description = form.description.data,
                    user_id = current_user.id,
                    renter_id = renter_id
                )
                db.session.add(payment)
                db.session.commit()
                return redirect(url_for('property_bp.renter', renter_id = renter_id))
            return render_template(
                'add_payment.jinja2',
                template = 'properties-page',
                form = form,
                renter_id = renter_id
            )
        flash("You do not have access to view this page")
        return redirect(url_for('property_bp.renters'))
    flash("U MUST BE LOGGED IN TO SEE THIS Pge")
    return redirect(url_for('auth_bp.login'))   # Send to login page if not logged in
    

#Functions
def convert_to_binary_data(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binary_data = file.read()
    return binary_data
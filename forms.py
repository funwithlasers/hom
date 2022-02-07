"""Sign-up & log-in forms."""
import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
# from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, FileField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from wtforms.fields.html5 import DateField


class SignupForm(FlaskForm):
    """User Sign-up Form."""
    first_name = StringField(
        'First Name',
        validators=[DataRequired()])
    last_name = StringField(
        'LastName',
        validators=[DataRequired()])
    email = StringField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Select a stronger password.')
        ]
    )
    confirm = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    website = StringField(
        'Website',
        validators=[Optional()]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email.')
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class PropertyForm(FlaskForm):
    """User Sign-up Form."""

    STATES = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
    street = StringField(
        label = 'Street',
        validators = [DataRequired()])
    city = StringField(
        label = 'City',
        validators=[DataRequired()])
    state = SelectField(
        label = 'State', 
        choices = STATES) # TODO: handle default/required
    zip = IntegerField(
        label = 'Zip',
        validators = [DataRequired()]
        # TODO: set limits
    )
    image = FileField('image', 
    validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')])

    submit = SubmitField('Register')


class RenterForm(FlaskForm):
    """Renter form"""
    first_name = StringField(
        'First Name',
        validators=[DataRequired()])
    last_name = StringField(
        'Last Name',
        validators=[DataRequired()])
    email = StringField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email'),
            DataRequired()])
    phone = StringField(
        'Phone Number',
        validators=[DataRequired()])

    submit = SubmitField('Add renter')


class LeaseForm(FlaskForm):
    """Lease  form"""
    renters = []
    start_date = DateField(
        'Start Date',
        validators=[DataRequired()])
    end_date = DateField(
        'End Date',
        validators=[DataRequired()])
    rate = DecimalField(
        'Rate', 
        places=2, 
        rounding=None, 
        validators=[DataRequired()])
    terms = IntegerField(
        'Terms',
        validators=[DataRequired()])
    renter = SelectField(
        label = 'Renter', 
        choices = renters) 

    submit = SubmitField('Add lease')


class PaymentForm(FlaskForm):
    """Payment  form"""
    date = DateField(
        'Payment Date',
        validators=[DataRequired()])
    amount = DecimalField(
        'Amount', 
        places=2, 
        rounding=None, 
        validators=[DataRequired()])
    description = StringField(
        'Description'
    )

    submit = SubmitField('Add payment')
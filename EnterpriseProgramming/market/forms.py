from flask_wtf import FlaskForm
from sqlalchemy import null
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import Item, User

class ItemForm(FlaskForm):
    def validate_name(self, name_to_check):
        item = Item.query.filter_by(name=name_to_check.data).first()
        if item:
            raise ValidationError('Item already exists! Please input a new item')

    def validate_barcode(self, barcode_to_check):
        barcode = Item.query.filter_by(barcode=barcode_to_check.data).first()
        if barcode:
            raise ValidationError('Barcode already exists! Please try a different barcode')
    
    def validate_description(self, description_to_check):
        description = Item.query.filter_by(description=description_to_check.data).first()
        if description:
            raise ValidationError('Description already exists! Please try a different description')

    name = StringField(label='Name:', validators=[Length(min=2, max=30), DataRequired()])
    country_appeal_rate = StringField(label='Country_appeal_rate:', validators=[Length(min=2, max=30), DataRequired()])
    category = StringField(label='Category:', validators=[Length(min=2, max=30), DataRequired()])
    price = StringField(label='Price:', validators=[Length(min=1), DataRequired()])
    barcode = StringField(label='Barcode:', validators=[Length(min=5, max=12), DataRequired()])
    description = StringField(label='Description:', validators=[Length(min=5, max=1024), DataRequired()])
    submit = SubmitField(label='Create Item')

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')
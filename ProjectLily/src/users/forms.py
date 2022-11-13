from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from src.models import User
from flask_login import current_user

class SignupForm(FlaskForm):
    """
        Sign up form
    """
    firstname = StringField('First Name', validators=[DataRequired(), Length(max=16)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(max=16)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=16)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=16), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_phone(self, phone):
        """
            Validate the phone number provided
        """
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('Phone number already in use, try again')

    def validate_email(self, email):
        """
            Validate the email provided
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email address already in use, try again')

class SigninForm(FlaskForm):
    """
        Sign in form
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=16)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class UpdateForm(FlaskForm):
    """
        Update account details form
    """
    name = StringField('Name', validators=[DataRequired(), Length(max=33)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_phone(self, phone):
        if phone.data != current_user.phone:
            user = User.query.filter_by(phone=phone.data).first()
            if user:
                raise ValidationError('Phone number already in use, try again')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email address already in use, try again')

class ContactForm(FlaskForm):
    """
        Contact form
    """
    subject = StringField('Subject', validators=[DataRequired(), Length(max=100)])
    email_content = TextAreaField('Content of Email', validators=[DataRequired()])
    submit = SubmitField('Send')

class ContactFormLoggedOut(FlaskForm):
    """
        Contact form when logged out (not signed in)
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone Number', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired(), Length(max=100)])
    email_content = TextAreaField('Content of Email', validators=[DataRequired()])
    submit = SubmitField('Send')

class RequestPasswordResetForm(FlaskForm):
    """
        Request a password reset link form
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request New Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('No account exists with this email. Register first.')

class ResetPasswordForm(FlaskForm):
    """
        Reset password form
    """
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=16)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=16), EqualTo('password')])
    submit = SubmitField('Reset Password')

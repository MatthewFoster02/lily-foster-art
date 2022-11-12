from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from src.users.util import send_contact_email, send_password_reset_email
from src.models import User
from src.users.forms import SigninForm, SignupForm, ContactForm, UpdateForm, RequestPasswordResetForm, ResetPasswordForm
from src import db, bcrypt


users = Blueprint('users', __name__)

@users.route("/contact", methods=['GET', 'POST'])
@login_required
def contact():
    """
        Contact route
    """
    form = ContactForm()
    if form.validate_on_submit():
        send_contact_email(current_user, form.subject.data, form.email_content.data)
        flash('Email sent! Thanks for getting in touch!', 'success')
        return redirect(url_for('main.index'))
    return render_template('contact.html', title="Contact", form=form)

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """
        Account route
    """
    form = UpdateForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Account info updated successfully', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.phone.data = current_user.phone
    return render_template('account.html', title="Account", form=form)

@users.route("/signin", methods=['GET', 'POST'])
def signin():
    """
        Sign in route
    """
    if current_user.is_authenticated:
        flash('You are already signed in', 'info')
        return redirect(url_for('main.index'))

    signin_form = SigninForm()

    if signin_form.validate_on_submit():
        user = User.query.filter_by(email=signin_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, signin_form.password.data):
            login_user(user, remember=signin_form.remember.data)
            next_page = request.args.get('next')
            flash('You have been signed in successfully!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Sign in unsuccessful, check email and password.', 'danger')

    return render_template('signin.html', title="Sign in", in_form=signin_form)

@users.route("/signup", methods=['GET', 'POST'])
def signup():
    """
        Sign up route
    """
    if current_user.is_authenticated:
        flash('You are already signed in', 'info')
        return redirect(url_for('main.index'))

    signup_form = SignupForm()

    if signup_form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(signup_form.password.data).decode('utf-8') # string representation
        name = signup_form.firstname.data + " " + signup_form.lastname.data
        user = User(name=name, email=signup_form.email.data, phone=signup_form.phone.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'{signup_form.firstname.data}, your account has been successfully created. You can now Sign In', 'success')
        return redirect(url_for('users.signin'))

    return render_template('signup.html', title="Sign up", up_form=signup_form)

@users.route('/signout')
def signout():
    """
        Sign out route
    """
    logout_user()
    flash('You have signed out successfully.', 'success')
    return redirect(url_for('main.index'))

@users.route('/request_password_reset', methods=['GET', 'POST'])
def request_password_reset():
    """
        Request password reset route
    """
    form = RequestPasswordResetForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_password_reset_email(user)
        flash(f'An email has been sent to {form.email.data}, there you will find a link to reset your password.', 'info')
        if current_user.is_authenticated:
            return redirect(url_for('users.account'))
        else:
            return redirect(url_for('users.signin'))
    
    return render_template('request_password_reset.html', title='Reset Password', form=form)

@users.route('/request_password_reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """
        Reset password route
    """
    user_id = User.verify_reset_token(token)
    if not user_id:
        flash('The reset link is invalid or has expired', 'danger')
        return redirect(url_for('users.request_password_reset'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_id.password = password_hash
        db.session.commit()
        flash('Your password has been updated successfully', 'success')
        if current_user.is_authenticated:
            return redirect(url_for('users.account'))
        else:
            return redirect(url_for('users.signin'))
    return render_template('reset_password.html', title='Reset Password', form=form)

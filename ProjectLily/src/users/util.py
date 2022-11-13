from flask_mail import Message
from flask import url_for
from src import mail, app_email
from flask import current_app
import jwt

#Send email to self, with the content from contact form
def send_contact_email(user, subject, content):
    email_msg = Message(subject, sender='lilyfosterart.business@gmail.com', recipients=[app_email])
    email_msg.body = f'''{content}

User Details:
Name: {user.name}
Email: {user.email}
Phone: {user.phone}
'''
    mail.send(email_msg)

# Send reset link via email
def send_password_reset_email(user):
    token = user.get_reset_token()
    email_msg = Message('Reset Password Link', sender='noreply.lilyfosterart.business@gmail.com', recipients=[user.email])
    email_msg.body = f'''Follow the link below to reset your password:

{url_for('users.reset_password', token=token, _external=True)}

If YOU did not ask for your password to be reset, you may simply ignore this email.
'''
    mail.send(email_msg)

# Generate email confirmation token
def get_confirmation_token(user_info):
        """
            Generates an email confirmation token, no expiration time
        """
        user_info_dict = {
                        'firstname': user_info.firstname.data,
                        'lastname': user_info.lastname.data,
                        'email': user_info.email.data,
                        'phone': user_info.phone.data,
                        'password': user_info.password.data
                        }
        token = jwt.encode(user_info_dict, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token

# Verify email confirmation token
def verify_confirmation_token(token):
    """
        Verifies the email confirmation token
    """
    try:
        user = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    except:
        return None
    return user

# Send email confirmation link to provided email
def send_email_confirmation(user_info):
    print(f"USER INFO: {user_info.firstname}, {user_info.email.data}")
    link_token = get_confirmation_token(user_info)
    email_msg = Message('Email Confirmation Link', sender='noreply.lilyfosterart.business@gmail.com', recipients=[user_info.email.data])
    email_msg.body = f'''Follow the link below to confirm your email and finish setting up your account:

{url_for('users.confirm_signup', token=link_token, _external=True)}

If you did not attempt to sign up to Lily Foster Art, then you may ignore this email.    
'''
    mail.send(email_msg)

def send_contact_email_logged_out(name, email, phone, subject, content):
    email_msg = Message(subject, sender='lilyfosterart.business@gmail.com', recipients=[app_email])
    email_msg.body = f'''{content}

User Details:
Name: {name}
Email: {email}
Phone: {phone}
'''
    mail.send(email_msg)

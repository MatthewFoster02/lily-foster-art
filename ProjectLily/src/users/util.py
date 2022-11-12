from flask_mail import Message
from flask import url_for
from src import mail, app_email

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
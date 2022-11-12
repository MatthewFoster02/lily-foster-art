import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from src.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.signin'
login_manager.login_message_category = 'warning'
mail = Mail()
app_email = os.environ.get('EMAIL_BUSINESS_LILY')

def createApp(configuration=Config):
    """
        Creates the application
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from src.users.routes import users
    from src.main.routes import main
    from src.art.routes import art
    from src.errors.error_handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(art)
    app.register_blueprint(errors)

    return app

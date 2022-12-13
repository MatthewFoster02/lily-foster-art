import jwt
from datetime import datetime, timezone, timedelta
from src import db, login_manager
from flask import current_app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """
        User database table
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    #cartItems = db.relationship('CartItem', backref='customer', lazy=True)

    def get_reset_token(self, expires_after_sec=300): # Default expires after 300 seconds, 5 minutes.
        """
            Generates the password reset token (jwt)
        """
        token = jwt.encode({'user_id': self.id, "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expires_after_sec)}, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token

    @staticmethod
    def verify_reset_token(token):
        """
            Verifies the reset token
        """
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.phone}')"

class ArtImages(db.Model):
    """
        Database table containing information on the art
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    filename = db.Column(db.String(200), unique=True, nullable=False)

    def __repr__(self):
        return f"Image('{self.title}', '{self.description}', '{self.filename}')"

class Products(db.Model):
    """
        Table containing all the prints for sale in the shop
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    previous_price = db.Column(db.Float)
    sale = db.Column(db.Boolean, nullable=False)
    sale_percent = db.Column(db.Integer)
    #cartItems = db.relationship('CartItem', backref='item', lazy=True)

    def __repr__(self):
        return f"Product('{self.title}', '{self.price}', '{self.sale}')"

class CartItem(db.Model):
    """
        Table which holds information about what products are in what carts
    """
    id = db.Column(db.Integer, primary_key=True)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

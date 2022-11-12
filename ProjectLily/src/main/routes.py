from flask import Blueprint, render_template


main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def index():
    """
        Home route (index)
    """
    return render_template('index.html', title="Home")

@main.route("/about")
def about():
    """
        About route
    """
    return render_template('about.html', title="About")
from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(403)
def error403(error):
    """
        Error 403 route - invalid permission
    """
    return render_template('error_pages/403.html', title='Error 403'), 403

@errors.app_errorhandler(404)
def error404(error):
    """
        Error 404 - Page not found
    """
    return render_template('error_pages/404.html', title='Error 404'), 404

@errors.app_errorhandler(500)
def error500(error):
    """
        Error 500 - Server error
    """
    return render_template('error_pages/500.html', title='Error 500'), 500

from flask import abort
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required

from functools import wraps

admin = Blueprint(
    'admin',
    __name__,
    template_folder="templates",
    static_folder='static',
)


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)
        return func(*args, **kwargs)
    return decorated_view


@admin.route('/')
@login_required
@admin_required
def index():
    """Admin dashboard."""
    return render_template('admin_dashboard.jinja2')

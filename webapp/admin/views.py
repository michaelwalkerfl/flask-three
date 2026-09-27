from datetime import UTC, datetime, timedelta
from functools import wraps

from flask import Blueprint, abort, render_template, request
from flask_login import current_user, login_required

from webapp.models.user import Role, User

admin = Blueprint(
    'admin',
    __name__,
    template_folder='templates',
    static_folder='static',
)

USERS_PER_PAGE = 20


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)
        return func(*args, **kwargs)

    return decorated_view


@admin.route('/', methods=['GET'])
@login_required
@admin_required
def index():
    """Admin dashboard."""
    week_ago = datetime.now(UTC) - timedelta(days=7)
    stats = {
        'total_users': User.query.count(),
        'admins': User.query.filter(User.roles.any(Role.name == 'admin')).count(),
        'new_this_week': User.query.filter(User.created_on >= week_ago).count(),
        'active_this_week': User.query.filter(User.last_login >= week_ago).count(),
    }
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_on.desc(), User.id.desc()).paginate(
        page=page, per_page=USERS_PER_PAGE, error_out=False
    )
    return render_template('admin_dashboard.jinja2', stats=stats, users=users)

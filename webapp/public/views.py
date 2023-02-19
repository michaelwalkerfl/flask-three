from flask import Blueprint
from flask import render_template

public = Blueprint(
    'public',
    __name__,
    template_folder="templates",
    static_folder='static',
)


@public.route('/', methods=['GET'])
def index():
    return render_template('index.jinja2')

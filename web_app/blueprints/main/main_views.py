from flask import Blueprint, render_template


blueprint = Blueprint('main', __name__)


@blueprint.route('/', methods=["GET"])
def index():
    return render_template('main.html')

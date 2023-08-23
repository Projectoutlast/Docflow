from flask import Blueprint, render_template
from flask_login import login_required


blueprint = Blueprint('work', __name__)


@blueprint.route('/workspace', methods=['GET', 'POST'])
@login_required
def home_workspace():
    return render_template('work/home.html')

from flask import Blueprint, render_template
from flask_login import current_user, login_required

from web_app.models import Employee


blueprint = Blueprint("work", __name__)


@blueprint.route("/workspace", methods=["GET", "POST"])
@login_required
def home_workspace():
    user_name = Employee.query.filter(Employee.id == current_user.id).first()
    return render_template('work/home.html', name=user_name.first_name)


@blueprint.route("/activities/all", methods=["GET"])
@login_required
def activities_all():
    return render_template("work/activities_main.html")


@blueprint.route("/activities/new/call", methods=["GET", "POST"])
@login_required
def activities_new_call():
    return render_template("work/activities_new_call.html")


@blueprint.route("/activities/new/meeting", methods=["GET", "POST"])
@login_required
def activities_new_meeting():
    return render_template("work/activities_new_meeting.html")


@blueprint.route("/activities/new/task", methods=["GET", "POST"])
@login_required
def activities_new_task():
    return render_template("work/activities_new_task.html")

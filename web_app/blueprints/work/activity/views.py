import sqlalchemy.exc
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from web_app import db
from web_app.models import CallActivity, Employee, MeetingActivity, TaskActivity
from web_app.blueprints.work.activity.forms import (combine_date_time, get_all_executors, get_executor,
                                                    NewActivityCall, NewActivityMeeting, NewActivityTask)


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
    form = NewActivityCall(request.form)
    form.executor.choices = get_all_executors(current_user.id)
    if form.validate_on_submit():
        employee = Employee.query.filter(Employee.id == current_user.id).first()
        if employee:
            try:
                new_call = CallActivity(company_id=employee.company_id,
                                        to_whom=form.to_whom.data,
                                        activity_holder=current_user.id,
                                        executor=get_executor(form),
                                        finish_until=combine_date_time(form.when_date.data, form.when_time.data))
                db.session.add(new_call)
                db.session.commit()

                flash("A new activity Call was created!", "success")
                return redirect(url_for("work.activities_all"))
            except sqlalchemy.exc.IntegrityError:
                db.session.rollback()
                flash("Invalid data was passed, try again!", "danger")
                return render_template("work/activities_new_call.html", form=form), 500
    return render_template("work/activities_new_call.html", form=form)


@blueprint.route("/activities/new/meeting", methods=["GET", "POST"])
@login_required
def activities_new_meeting():
    form = NewActivityMeeting(request.form)
    form.executor.choices = get_all_executors(current_user.id)
    if form.validate_on_submit():
        employee = Employee.query.filter(Employee.id == current_user.id).first()
        if employee:
            try:
                new_meeting = MeetingActivity(company_id=employee.company_id,
                                              activity_holder=current_user.id,
                                              with_whom=form.with_whom.data,
                                              location=form.location.data,
                                              executor=get_executor(form),
                                              finish_until=combine_date_time(form.when_date.data, form.when_time.data))
                db.session.add(new_meeting)
                db.session.commit()

                flash("A new activity Meeting was created!", "success")
                return redirect(url_for("work.activities_all"))
            except sqlalchemy.exc.IntegrityError:
                db.session.rollback()
                flash("Invalid data was passed, try again!", "danger")
                return render_template("work/activities_new_meeting.html", form=form), 500
    return render_template("work/activities_new_meeting.html", form=form)


@blueprint.route("/activities/new/task", methods=["GET", "POST"])
@login_required
def activities_new_task():
    form = NewActivityTask(request.form)
    form.executor.choices = get_all_executors(current_user.id)
    if form.validate_on_submit():
        employee = Employee.query.filter(Employee.id == current_user.id).first()
        if employee:
            try:
                new_meeting = TaskActivity(company_id=employee.company_id,
                                           subject=form.subject.data,
                                           describe=form.describe.data,
                                           activity_holder=current_user.id,
                                           executor=get_executor(form),
                                           finish_until=combine_date_time(form.when_date.data, form.when_time.data))
                db.session.add(new_meeting)
                db.session.commit()

                flash("A new activity Task was created!", "success")
                return redirect(url_for("work.activities_all"))
            except sqlalchemy.exc.IntegrityError:
                db.session.rollback()
                flash("Invalid data was passed, try again!", "danger")
                return render_template("work/activities_new_task.html", form=form), 500
    return render_template("work/activities_new_task.html", form=form)

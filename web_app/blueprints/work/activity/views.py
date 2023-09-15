import enum

import sqlalchemy.exc
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from web_app import db
from web_app.enums import ActivityStatus, TypeOfActivity
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
    all_calls = CallActivity.query.filter(CallActivity.activity_holder == current_user.id,
                                          CallActivity.status == ActivityStatus.IN_PROGRESS).all()
    all_meetings = MeetingActivity.query.filter(MeetingActivity.activity_holder == current_user.id,
                                                MeetingActivity.status == ActivityStatus.IN_PROGRESS).all()
    all_tasks = TaskActivity.query.filter(TaskActivity.activity_holder == current_user.id,
                                          TaskActivity.status == ActivityStatus.IN_PROGRESS).all()
    activities = [*all_calls, *all_meetings, *all_tasks]
    return render_template("work/activities_main.html", activities=activities)


@blueprint.route("/activities/new/call", methods=["GET", "POST"])
@login_required
def activities_new_call():
    form = NewActivityCall(request.form)
    form.executor.choices = get_all_executors(current_user.id)
    if form.validate_on_submit():
        employee = Employee.query.filter(Employee.id == current_user.id).first()
        executor = Employee.query.filter(Employee.id == get_executor(form)).first()
        if employee:
            try:
                new_call = CallActivity(company_id=employee.company_id,
                                        to_whom=form.to_whom.data,
                                        activity_holder=current_user.id,
                                        activity_holder_name=f"{employee.first_name} {employee.last_name}",
                                        executor=get_executor(form),
                                        executor_name=f"{executor.first_name} {executor.last_name}",
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
        executor = Employee.query.filter(Employee.id == get_executor(form)).first()
        if employee:
            try:
                new_meeting = MeetingActivity(company_id=employee.company_id,
                                              activity_holder=current_user.id,
                                              activity_holder_name=f"{employee.first_name} {employee.last_name}",
                                              with_whom=form.with_whom.data,
                                              location=form.location.data,
                                              executor=get_executor(form),
                                              executor_name=f"{executor.first_name} {executor.last_name}",
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
        executor = Employee.query.filter(Employee.id == get_executor(form)).first()
        if employee:
            try:
                new_meeting = TaskActivity(company_id=employee.company_id,
                                           subject=form.subject.data,
                                           describe=form.describe.data,
                                           activity_holder=current_user.id,
                                           activity_holder_name=f"{employee.first_name} {employee.last_name}",
                                           executor=get_executor(form),
                                           executor_name=f"{executor.first_name} {executor.last_name}",
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


@blueprint.route("/activities/complete/<string:activity_type>/<int:activity_id>", methods=["POST", "GET"])
@login_required
def activities_complete_process(activity_type: str, activity_id: int):
    entity = None
    match activity_type:
        case TypeOfActivity.CALL.value:
            entity = CallActivity.query.filter(CallActivity.id == activity_id).first()
        case TypeOfActivity.MEETING.value:
            entity = MeetingActivity.query.filter(MeetingActivity.id == activity_id).first()
        case TypeOfActivity.TASK.value:
            entity = TaskActivity.query.filter(TaskActivity.id == activity_id).first()
    if entity:
        entity.status = ActivityStatus.COMPLETE
        try:
            db.session.add(entity)
            db.session.commit()

            flash("Activity completed", "success")
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash("Something went wrong", "danger")

        return redirect(url_for("work.activities_all"))

    flash(f"Activity with Id={activity_id} not found", "warning")
    return redirect(url_for("work.activities_all")), 404


@blueprint.route("/activities/completed/all", methods=["GET"])
def activities_completed_all():
    all_calls = CallActivity.query.filter(CallActivity.activity_holder == current_user.id,
                                          CallActivity.status == ActivityStatus.COMPLETE).all()
    all_meetings = MeetingActivity.query.filter(MeetingActivity.activity_holder == current_user.id,
                                                MeetingActivity.status == ActivityStatus.COMPLETE).all()
    all_tasks = TaskActivity.query.filter(TaskActivity.activity_holder == current_user.id,
                                          TaskActivity.status == ActivityStatus.COMPLETE).all()
    activities = [*all_calls, *all_meetings, *all_tasks]
    return render_template("work/activities_completed.html", activities=activities)


@blueprint.route("/activities/cancel/<int:activities_id>", methods=["POST", "GET"])
@login_required
def activities_cancel(activities_id: int):
    return redirect(url_for("work.activities_all"))


@blueprint.route("/activities/extend-date/<int:activities_id>", methods=["POST", "GET"])
@login_required
def activities_extend(activities_id: int):
    return redirect(url_for("work.activities_all"))

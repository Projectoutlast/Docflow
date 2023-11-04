import datetime

import sqlalchemy.exc

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_

from web_app import db
from web_app.enums import ActivityStatus, TypeOfActivity
from web_app.models import CallActivity, Employee, MeetingActivity, TaskActivity
from web_app.blueprints.work.activity.forms import (combine_date_time, get_all_executors, get_executor,
                                                    ActivityCall, ActivityCallEdit, ActivityMeeting,
                                                    ActivityMeetingEdit, ActivityTask, ActivityTaskEdit)
from web_app.utils.utilities import check_overdue_activities, email_confirm, get_activity


blueprint = Blueprint("work", __name__)


@blueprint.route("/unconfirmed-workspace", methods=["GET"])
@login_required
def unconfirmed_workspace():
    if current_user.is_confirmed:
        flash("Account already confirmed.", "success")
        return redirect(url_for("work.home_workspace"))
    return render_template("work/home_unconfirmed_page.html")


@blueprint.route("/workspace", methods=["GET", "POST"])
@email_confirm
@login_required
def home_workspace():
    user_name = Employee.query.filter(Employee.id == current_user.id).first()
    return render_template('work/home.html', name=user_name.first_name)


@blueprint.route("/activities/all", methods=["GET"])
@email_confirm
@login_required
def activities_all():

    check_overdue_activities(current_user.id)

    all_calls = CallActivity.query.filter(CallActivity.executor == current_user.id,
                                          or_(CallActivity.status == ActivityStatus.IN_PROGRESS,
                                              CallActivity.status == ActivityStatus.OVERDUE)).all()

    all_meetings = MeetingActivity.query.filter(MeetingActivity.executor == current_user.id,
                                                or_(MeetingActivity.status == ActivityStatus.IN_PROGRESS,
                                                    MeetingActivity.status == ActivityStatus.OVERDUE)).all()

    all_tasks = TaskActivity.query.filter(TaskActivity.executor == current_user.id,
                                          or_(TaskActivity.status == ActivityStatus.IN_PROGRESS,
                                              TaskActivity.status == ActivityStatus.OVERDUE)).all()

    activities = [*all_calls, *all_meetings, *all_tasks]
    return render_template("work/activities_main.html", activities=activities)


@blueprint.route("/activities/new/call", methods=["GET", "POST"])
@email_confirm
@login_required
def activities_new_call():
    form = ActivityCall(request.form)
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
@email_confirm
@login_required
def activities_new_meeting():
    form = ActivityMeeting(request.form)
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
@email_confirm
@login_required
def activities_new_task():
    form = ActivityTask(request.form)
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
@email_confirm
@login_required
def activities_complete_process(activity_type: str, activity_id: int):
    entity = get_activity(activity_type, activity_id)
    if entity:
        entity.status = ActivityStatus.COMPLETE
        try:
            db.session.add(entity)
            db.session.commit()

            flash("Activity completed", "success")
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash("Something went wrong", "danger")

        if request.referrer is None:
            return redirect(url_for("work.activities_all"))
        elif "overdue/all" in request.referrer:
            return redirect(url_for("work.activities_overdue_all"))
        else:
            return redirect(url_for("work.activities_all"))

    flash(f"Activity with Id={activity_id} not found", "warning")
    return redirect(url_for("work.activities_all")), 404


@blueprint.route("/activities/completed/all", methods=["GET"])
@email_confirm
@login_required
def activities_completed_all():
    all_calls = CallActivity.query.filter(CallActivity.activity_holder == current_user.id,
                                          CallActivity.status == ActivityStatus.COMPLETE).all()
    all_meetings = MeetingActivity.query.filter(MeetingActivity.activity_holder == current_user.id,
                                                MeetingActivity.status == ActivityStatus.COMPLETE).all()
    all_tasks = TaskActivity.query.filter(TaskActivity.activity_holder == current_user.id,
                                          TaskActivity.status == ActivityStatus.COMPLETE).all()
    activities = [*all_calls, *all_meetings, *all_tasks]
    return render_template("work/activities_completed.html", activities=activities)


@blueprint.route("/activities/overdue/all", methods=["GET"])
@email_confirm
@login_required
def activities_overdue_all():
    all_calls = CallActivity.query.filter(CallActivity.activity_holder == current_user.id,
                                          CallActivity.status == ActivityStatus.OVERDUE).all()
    all_meetings = MeetingActivity.query.filter(MeetingActivity.activity_holder == current_user.id,
                                                MeetingActivity.status == ActivityStatus.OVERDUE).all()
    all_tasks = TaskActivity.query.filter(TaskActivity.activity_holder == current_user.id,
                                          TaskActivity.status == ActivityStatus.OVERDUE).all()
    activities = [*all_calls, *all_meetings, *all_tasks]
    return render_template("work/activities_overdue.html", activities=activities)


@blueprint.route("/activities/cancel/<string:activity_type>/<int:activity_id>", methods=["POST", "GET"])
@email_confirm
@login_required
def activities_cancel(activity_type: str, activity_id: int):
    entity = get_activity(activity_type, activity_id)
    if entity:
        try:
            db.session.delete(entity)
            db.session.commit()

            flash("Activity successful deleted", "success")
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash("Something went wrong", "danger")

        if request.referrer is None:
            return redirect(url_for("work.activities_all"))
        if "overdue/all" in request.referrer:
            return redirect(url_for("work.activities_overdue_all"))
        elif "/all" in request.referrer:
            return redirect(url_for("work.activities_all"))

    flash(f"Activity with Id={activity_id} not found", "warning")
    return redirect(url_for("work.activities_all")), 404


@blueprint.route("/activities/extend-date/<int:activities_id>", methods=["POST", "GET"])
@email_confirm
@login_required
def activities_extend(activities_id: int):
    return redirect(url_for("work.activities_all"))


@blueprint.route("/activities/<string:activity_type>/<int:activity_id>/info", methods=["GET", "POST"])
@email_confirm
@login_required
def get_activity_info(activity_type: str, activity_id: int):
    activity = get_activity(activity_type, activity_id)
    if activity:
        return render_template("work/activity_info.html", activity=activity)
    flash(f"Activity not found", "warning")
    return redirect(url_for("work.activities_all")), 404


@blueprint.route("/activities/task/<int:activity_id>/edit", methods=["GET", "POST"])
@email_confirm
@login_required
def activity_task_edit(activity_id: int):
    activity = get_activity(TypeOfActivity.TASK.value, activity_id)
    form = ActivityTaskEdit(request.form)
    if not activity:
        flash(f"Activity not found", "warning")
        return redirect(url_for("work.activities_all")), 404

    form.executor.choices = get_all_executors(current_user.id)
    form.describe.data = activity.describe
    form.when_date.data = datetime.datetime.strptime(str(activity.finish_until.date()), "%Y-%m-%d")
    form.when_time.data = datetime.datetime.strptime(str(activity.finish_until.time()), "%H:%M:%S").time()

    return render_template("work/activities_edit.html", activity=activity, form=form)


@blueprint.route("/activities/task/<int:activity_id>/update", methods=["POST"])
@email_confirm
@login_required
def activity_task_update(activity_id: int):
    activity = get_activity(TypeOfActivity.TASK.value, activity_id)
    form = ActivityTaskEdit(request.form)
    form.executor.choices = get_all_executors(current_user.id)
    if form.validate_on_submit():
        executor = Employee.query.filter(Employee.id == get_executor(form)).first()
        activity.subject = form.subject.data
        activity.describe = form.describe.data
        activity.executor = get_executor(form)
        activity.executor_name = f"{executor.first_name} {executor.last_name}"
        activity.finish_until = combine_date_time(form.when_date.data, form.when_time.data)
        try:
            db.session.commit()

            flash("An activity successfully updated!", "success")
            return redirect(url_for("work.activities_all"))
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash("Invalid data was passed, try again!", "danger")
            return render_template("work/activities_edit.html", form=form), 500
    return redirect(url_for("work.activity_task_edit", activity_id=activity_id, activity=activity))


@blueprint.route("/activities/call/<int:activity_id>/edit", methods=["GET", "POST"])
@email_confirm
@login_required
def activity_call_edit(activity_id: int):
    activity = get_activity(TypeOfActivity.CALL.value, activity_id)
    form = ActivityCallEdit(request.form)
    if not activity:
        flash(f"Activity not found", "warning")
        return redirect(url_for("work.activities_all")), 404

    form.executor.choices = get_all_executors(current_user.id)
    form.to_whom.data = activity.to_whom
    form.when_date.data = datetime.datetime.strptime(str(activity.finish_until.date()), "%Y-%m-%d")
    form.when_time.data = datetime.datetime.strptime(str(activity.finish_until.time()), "%H:%M:%S").time()

    return render_template("work/activities_edit.html", activity=activity, form=form)


@blueprint.route("/activities/call/<int:activity_id>/update", methods=["POST"])
@email_confirm
@login_required
def activity_call_update(activity_id: int):
    activity = get_activity(TypeOfActivity.CALL.value, activity_id)
    form = ActivityCallEdit(request.form)
    form.executor.choices = get_all_executors(current_user.id)
    if form.validate_on_submit():
        executor = Employee.query.filter(Employee.id == get_executor(form)).first()
        activity.to_whom = form.to_whom.data
        activity.executor = get_executor(form)
        activity.executor_name = f"{executor.first_name} {executor.last_name}"
        activity.finish_until = combine_date_time(form.when_date.data, form.when_time.data)
        try:
            db.session.commit()

            flash("An activity successfully updated!", "success")
            return redirect(url_for("work.activities_all"))
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash("Invalid data was passed, try again!", "danger")
            return render_template("work/activities_edit.html", form=form), 500
    return redirect(url_for("work.activity_call_edit", activity_id=activity_id, activity=activity))


@blueprint.route("/activities/meeting/<int:activity_id>/edit", methods=["GET", "POST"])
@email_confirm
@login_required
def activity_meeting_edit(activity_id: int):
    activity = get_activity(TypeOfActivity.MEETING.value, activity_id)
    form = ActivityMeetingEdit(request.form)
    if not activity:
        flash(f"Activity not found", "warning")
        return redirect(url_for("work.activities_all")), 404

    form.executor.choices = get_all_executors(current_user.id)
    form.with_whom.data = activity.with_whom
    form.location.data = activity.location
    form.when_date.data = datetime.datetime.strptime(str(activity.finish_until.date()), "%Y-%m-%d")
    form.when_time.data = datetime.datetime.strptime(str(activity.finish_until.time()), "%H:%M:%S").time()

    return render_template("work/activities_edit.html", activity=activity, form=form)


@blueprint.route("/activities/meeting/<int:activity_id>/update", methods=["POST"])
@email_confirm
@login_required
def activity_meeting_update(activity_id: int):
    activity = get_activity(TypeOfActivity.MEETING.value, activity_id)
    form = ActivityMeetingEdit(request.form)
    form.executor.choices = get_all_executors(current_user.id)
    if form.validate_on_submit():
        executor = Employee.query.filter(Employee.id == get_executor(form)).first()
        activity.with_whom = form.with_whom.data
        activity.location = form.location.data
        activity.executor = get_executor(form)
        activity.executor_name = f"{executor.first_name} {executor.last_name}"
        activity.finish_until = combine_date_time(form.when_date.data, form.when_time.data)
        try:
            db.session.commit()

            flash("An activity successfully updated!", "success")
            return redirect(url_for("work.activities_all"))
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash("Invalid data was passed, try again!", "danger")
            return render_template("work/activities_edit.html", form=form), 500
    return redirect(url_for("work.activity_meeting_edit", activity_id=activity_id, activity=activity))

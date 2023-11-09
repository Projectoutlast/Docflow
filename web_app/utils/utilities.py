import datetime
import pathlib
import secrets

from flask import current_app, flash, redirect, url_for
from flask_login import current_user
from functools import wraps

import sqlalchemy.exc

from config import Config
from web_app import db
from web_app.enums import ActivityStatus, TypeOfActivity
from web_app.models import CallActivity, MeetingActivity, TaskActivity


def check_overdue_activities(user_id: int) -> None:
    """
    Function check, if current datetime more than activity's finish until time, then switch activity status from
    In progress to Overdue
    """
    all_calls = CallActivity.query.filter(CallActivity.executor == user_id,
                                          CallActivity.status == ActivityStatus.IN_PROGRESS,
                                          CallActivity.finish_until < datetime.datetime.now()).all()
    all_meetings = MeetingActivity.query.filter(MeetingActivity.executor == user_id,
                                                MeetingActivity.status == ActivityStatus.IN_PROGRESS,
                                                MeetingActivity.finish_until < datetime.datetime.now()).all()
    all_tasks = TaskActivity.query.filter(TaskActivity.executor == user_id,
                                          TaskActivity.status == ActivityStatus.IN_PROGRESS,
                                          TaskActivity.finish_until < datetime.datetime.now()).all()
    result = []
    for one_call in all_calls:
        one_call.status = ActivityStatus.OVERDUE
        result.append(one_call)
    for one_meeting in all_meetings:
        one_meeting.status = ActivityStatus.OVERDUE
        result.append(one_meeting)
    for one_task in all_tasks:
        one_task.status = ActivityStatus.OVERDUE
        result.append(one_task)

    try:
        db.session.add_all(result)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
    return None


def get_activity(activity_type: str, activity_id: int) -> db.Model | None:
    """
    Get activity type, id and return db.Model activity
    """

    match activity_type:
        case TypeOfActivity.CALL.value:
            return CallActivity.query.filter(CallActivity.id == activity_id).first()
        case TypeOfActivity.MEETING.value:
            return MeetingActivity.query.filter(MeetingActivity.id == activity_id).first()
        case TypeOfActivity.TASK.value:
            return TaskActivity.query.filter(TaskActivity.id == activity_id).first()

    return None


def get_path_to_profile_photo(path: str) -> str:
    """
    Get path to profile photo for current user, check, if folder is existing or not.
    If exist - clear data in folder and return path for writing a new path for new profile photo
    If not exist - create a folder for a profile photo for the current user
    """
    if all([pathlib.Path(path).exists(), pathlib.Path(path).is_dir()]):
        delete_data_from_exact_folder(pathlib.Path(path))
        return str(path)
    pathlib.Path(path).mkdir(exist_ok=True)
    return str(path)


def delete_data_from_exact_folder(path: pathlib.Path) -> None:
    """
    Get path to directory and clear that one
    """
    for file in path.iterdir():
        file.unlink()
    return


def check_extension_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_UPLOAD_EXTENSIONS


def email_confirm(func):
    """
     The function checks if the user's email address is not verified and is redirected
     to a page with limited functionality.
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):

        if not current_user.is_confirmed:
            flash("Your email address isn't verified")
            return redirect(url_for("work.unconfirmed_workspace"))

        if callable(getattr(current_app, "ensure_sync", None)):
            return current_app.ensure_sync(func)(*args, **kwargs)
        return func(*args, **kwargs)

    return decorated_view


def generate_new_password(pwd_length: int = Config.PWD_LENGTH) -> str:
    """
    Generate a new password for the user who resets his password
    """
    result = ""
    for i in range(pwd_length):
        result += "".join(secrets.choice(Config.PWD_GENERATE_ALPHABET))
    return result

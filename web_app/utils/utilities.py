import datetime

import sqlalchemy.exc

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

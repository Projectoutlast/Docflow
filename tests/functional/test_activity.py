import datetime

from sqlalchemy import or_

from tests.utils_for_tests import TEST_DATE_WHEN, TEST_TIME_WHEN
from web_app.enums import ActivityStatus, TypeOfActivity
from web_app.models import CallActivity, MeetingActivity, TaskActivity


def test_activities_pages(test_auth_client):
    """
   GIVEN a Flask application
   WHEN user is logged in
   THEN check that all activities page work correct
   """

    response = test_auth_client.get("/activities/all", follow_redirects=True)
    assert response.status_code == 200
    assert b"New activity" in response.data

    response = test_auth_client.get("/activities/new/call", follow_redirects=True)
    assert response.status_code == 200
    assert (b"To whom" and b"When" and b"Create") in response.data

    response = test_auth_client.get("/activities/new/meeting", follow_redirects=True)
    assert response.status_code == 200
    assert (b"With whom" and b"Location" and b"Create") in response.data

    response = test_auth_client.get("/activities/new/task", follow_redirects=True)
    assert response.status_code == 200
    assert (b"Subject" and b"Describe" and b"Create") in response.data


def test_activities_manipulate(test_auth_client):
    """
   GIVEN a Flask application
   WHEN user is logged in
   THEN check that all manipulates with activities work correct
   """
    response = None

    calls = CallActivity.query.filter(or_(CallActivity.status == ActivityStatus.IN_PROGRESS,
                                          CallActivity.status == ActivityStatus.OVERDUE)).all()
    meetings = MeetingActivity.query.filter(or_(MeetingActivity.status == ActivityStatus.IN_PROGRESS,
                                                MeetingActivity.status == ActivityStatus.OVERDUE)).all()
    tasks = TaskActivity.query.filter(or_(MeetingActivity.status == ActivityStatus.IN_PROGRESS,
                                          MeetingActivity.status == ActivityStatus.OVERDUE)).all()
    assert len(calls) == 25
    assert len(meetings) == 25
    assert len(tasks) == 25

    for i in range(1, 6):
        test_auth_client.post(f"/activities/complete/{TypeOfActivity.CALL.value}/{i}", follow_redirects=True)
    calls_in_progress = CallActivity.query.filter(CallActivity.status == ActivityStatus.IN_PROGRESS).all()
    calls_completed = CallActivity.query.filter(CallActivity.status == ActivityStatus.COMPLETE).all()
    assert len(calls_in_progress) == 15
    assert len(calls_completed) == 5

    for i in range(1, 6):
        test_auth_client.post(f"/activities/complete/{TypeOfActivity.MEETING.value}/{i}",
                                         follow_redirects=True)
    meetings_in_progress = MeetingActivity.query.filter(MeetingActivity.status == ActivityStatus.IN_PROGRESS).all()
    meetings_completed = MeetingActivity.query.filter(MeetingActivity.status == ActivityStatus.COMPLETE).all()
    assert len(meetings_in_progress) == 15
    assert len(meetings_completed) == 5

    for i in range(1, 6):
        test_auth_client.post(f"/activities/complete/{TypeOfActivity.TASK.value}/{i}", follow_redirects=True)
    tasks_in_progress = TaskActivity.query.filter(TaskActivity.status == ActivityStatus.IN_PROGRESS).all()
    tasks_completed = TaskActivity.query.filter(TaskActivity.status == ActivityStatus.IN_PROGRESS).all()
    assert len(tasks_in_progress) == 15
    assert len(tasks_completed) == 15

    response = test_auth_client.get("/activities/overdue/all", follow_redirects=True)
    assert response.status_code == 200
    assert b"overdue" in response.data

    response = test_auth_client.get("/activities/completed/all", follow_redirects=True)
    assert response.status_code == 200

    response = test_auth_client.post(f"/activities/complete/{TypeOfActivity.CALL.value}/{100}", follow_redirects=True)
    assert response.status_code == 404

    response = test_auth_client.post(f"/activities/complete/{TypeOfActivity.MEETING.value}/{100}",
                                     follow_redirects=True)
    assert response.status_code == 404

    response = test_auth_client.post(f"/activities/complete/{TypeOfActivity.TASK.value}/{100}", follow_redirects=True)
    assert response.status_code == 404


def test_activities_form(test_auth_client):
    """
   GIVEN a Flask application
   WHEN user is logged in
   THEN check that all activities form work correct
   """

    response = test_auth_client.get("/activities/all", follow_redirects=True)
    assert b"John Due" in response.data

    call_payload = {"to_whom": "Mr. Smith",
                    "when_date": TEST_DATE_WHEN,
                    "when_time": TEST_TIME_WHEN.strftime("%H:%M"),
                    "executor": 1,
                    "myself": True}
    response = test_auth_client.post("/activities/new/call", data=call_payload, follow_redirects=True)
    call = CallActivity.query.filter(CallActivity.to_whom == "Mr. Smith").first()
    assert response.status_code == 200
    assert b"A new activity Call was created!" in response.data
    assert call.to_whom == "Mr. Smith"
    assert call.finish_until == datetime.datetime(2024, 12, 31, 12, 0)

    meeting_payload = {"with_whom": "Neo",
                       "location": "Matrix",
                       "when_date": TEST_DATE_WHEN,
                       "when_time": TEST_TIME_WHEN.strftime("%H:%M"),
                       "executor": 1,
                       "myself": False}
    response = test_auth_client.post("/activities/new/meeting", data=meeting_payload, follow_redirects=True)
    meeting = MeetingActivity.query.filter(MeetingActivity.location == "Matrix").first()
    assert response.status_code == 200
    assert b"A new activity Meeting was created!" in response.data
    assert meeting.with_whom == "Neo"
    assert meeting.finish_until == datetime.datetime(2024, 12, 31, 12, 0)

    task_payload = {"subject": "Month Report",
                    "describe": "Need to get information from analytic department",
                    "when_date": TEST_DATE_WHEN,
                    "when_time": TEST_TIME_WHEN.strftime("%H:%M"),
                    "executor": 12,
                    "myself": True}
    response = test_auth_client.post("/activities/new/task", data=task_payload, follow_redirects=True)
    task = TaskActivity.query.filter(TaskActivity.subject == "Month Report").first()
    assert response.status_code == 200
    assert b"A new activity Task was created!" in response.data
    assert task.activity_holder == 1
    assert task.finish_until == datetime.datetime(2024, 12, 31, 12, 0)

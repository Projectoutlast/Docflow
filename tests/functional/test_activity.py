import datetime

from tests.utils_for_tests import TEST_DATE_WHEN, TEST_TIME_WHEN
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


def test_activities_form(test_auth_client):
    """
   GIVEN a Flask application
   WHEN user is logged in
   THEN check that all activities form work correct
   """

    response = test_auth_client.get("/activities/all", follow_redirects=True)
    assert b"Teresa May" and b"Mr Andersen" and b"Agent Smith" in response.data

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

import datetime

import pytest

from web_app.models import CallActivity, Company, Employee, MeetingActivity, TaskActivity


@pytest.fixture
def new_company():
    """Create new Company instance"""
    company = Company(company_name="Smart", tax_id_number=453380, company_email="smart@example.com")
    return company


@pytest.fixture
def new_employee():
    """Create new Employee instance"""
    employee = Employee(
        first_name="Jack", last_name="Sparrow", email="jack@example.com", password="test")  # type: ignore
    employee.generate_password_hash("test")
    return employee


def test_new_company(new_company):
    """
    GIVEN a Company model
    WHEN a new Company is created
    THEN check the company_name, tax_id_number and company_email fields are defined correctly
    """
    assert new_company.company_name == "Smart"
    assert new_company.tax_id_number == 453380
    assert new_company.company_email == "smart@example.com"
    assert str(new_company) == f"<Company name {new_company.company_name}, email {new_company.company_email}>"


def test_new_employee(new_employee):
    """
    GIVEN an Employee model
    WHEN a new Employee is created
    THEN check the check_password_hash method work correct, first_name, last_name and password fields are
    defined correctly
    """
    assert new_employee.check_password_hash("test") is True
    assert new_employee.check_password_hash("sdfsdfdsfsdf") is False
    assert new_employee.password != "test"
    assert new_employee.first_name == "Jack"
    assert new_employee.last_name == "Sparrow"
    assert str(new_employee) == f"<User Id={new_employee.id}, company-{new_employee.company_id}>"


@pytest.fixture
def new_activity_call():
    """Create new CallActivity instance"""
    call_activity = CallActivity(company_id=1, to_whom="Mr. Smith", activity_holder=2, executor=2,
                                 finish_until=datetime.datetime(2024, 12, 31, 12, 0, 0),
                                 )
    return call_activity


def test_new_activity_call(new_activity_call):
    """
    GIVEN an CallActivity model
    WHEN a new CallActivity instance is created
    THEN check the fields are defined correctly
    """
    assert new_activity_call.id is None
    assert new_activity_call.company_id == 1
    assert new_activity_call.to_whom == "Mr. Smith"
    assert new_activity_call.activity_holder == 2
    assert new_activity_call.executor == 2
    assert new_activity_call.finish_until == datetime.datetime(2024, 12, 31, 12, 0, 0)
    assert str(new_activity_call) == f"<Id={new_activity_call.id}, activity_holder={new_activity_call.activity_holder}>"


@pytest.fixture
def new_activity_meeting():
    """Create new MeetingActivity instance"""
    meeting_activity = MeetingActivity(company_id=1, with_whom="Neo", location="Matrix", activity_holder=2, executor=2,
                                       finish_until=datetime.datetime(2024, 12, 31, 12, 0, 0))
    return meeting_activity


def test_new_activity_meeting(new_activity_meeting):
    """
    GIVEN an MeetingActivity model
    WHEN a new MeetingActivity instance is created
    THEN check the fields are defined correctly
    """
    assert new_activity_meeting.company_id == 1
    assert new_activity_meeting.with_whom == "Neo"
    assert new_activity_meeting.location == "Matrix"
    assert new_activity_meeting.activity_holder == 2
    assert new_activity_meeting.executor == 2
    assert new_activity_meeting.finish_until == datetime.datetime(2024, 12, 31, 12, 0, 0)
    assert str(new_activity_meeting) == (f"<Id={new_activity_meeting.id}, "
                                         f"activity_holder={new_activity_meeting.activity_holder}>")


@pytest.fixture
def new_activity_task():
    """Create new TaskActivity instance"""
    new_task = TaskActivity(company_id=1, subject="Month report", describe="Get information from analytic department",
                            activity_holder=2, executor=2, finish_until=datetime.datetime(2024, 12, 31, 12, 0, 0))
    return new_task


def test_new_activity_task(new_activity_task):
    """
    GIVEN an TaskActivity model
    WHEN a new TaskActivity instance is created
    THEN check the fields are defined correctly
    """
    assert new_activity_task.company_id == 1
    assert new_activity_task.subject == "Month report"
    assert "information from analytic" in new_activity_task.describe
    assert new_activity_task.activity_holder == 2
    assert new_activity_task.executor == 2
    assert new_activity_task.finish_until == datetime.datetime(2024, 12, 31, 12, 0, 0)
    assert str(new_activity_task) == f"<Id={new_activity_task.id}, activity_holder={new_activity_task.activity_holder}>"

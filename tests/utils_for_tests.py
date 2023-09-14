import datetime
import random
import sqlalchemy.exc

from faker import Faker

from web_app.blueprints.work.activity.forms import combine_date_time
from web_app.models import CallActivity, Company, Employee, MeetingActivity, TaskActivity
from web_app import db

fake = Faker()

TEST_DATE_WHEN = datetime.date(2024, 12, 31)
TEST_TIME_WHEN = datetime.time(12, 0, 0)


def generate_new_company() -> None:
    """
    Generate three new company for test cases
    """
    result = [Company(company_name=fake.company(), tax_id_number=777777, company_email="test@example.com")]
    for i in range(3):
        result.append(Company(company_name=fake.company(), tax_id_number=453380 + i, company_email=fake.email()))

    try:
        db.session.add_all(result)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
    return None


def generate_new_employee() -> None:
    """
    Generate thirty new employees. Ten employees for each company.
    """
    result = []
    entity = Employee(company_id=2, first_name="John",  # type: ignore
                      last_name="Due", email="john@example.com", password="123456")  # type: ignore
    entity.generate_password_hash(entity.password)
    result.append(entity)
    for i in range(3):
        for _ in range(10):
            entity = Employee(company_id=1 + i, first_name=fake.first_name(),  # type: ignore
                              last_name=fake.last_name(), email=fake.email(), password="123456")  # type: ignore
            entity.generate_password_hash(entity.password)
            result.append(entity)
    try:
        db.session.add_all(result)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
    return None


def generate_activities() -> None:
    """
     Generate activities for John Due
    """
    john_due = Employee.query.filter(Employee.email == "john@example.com").first()
    all_employee_id = [
        employee.id for employee in Employee.query.filter(Employee.company_id == john_due.company_id).all()]
    result = []
    for _ in range(10):
        call_entity = CallActivity(company_id=john_due.company_id,
                                   to_whom=fake.first_name(),
                                   activity_holder=john_due.id,
                                   activity_holder_name=f"{john_due.first_name} {john_due.last_name}",
                                   executor=random.randint(min(all_employee_id), max(all_employee_id)),
                                   executor_name="Agent Smith",
                                   finish_until=combine_date_time(fake.future_date(), datetime.time(
                                       random.randint(0, 23),
                                       random.randint(0, 59),
                                       random.randint(0, 59))))
        meeting_entity = MeetingActivity(company_id=john_due.company_id,
                                         with_whom=fake.first_name(),
                                         location=fake.city(),
                                         activity_holder=john_due.id,
                                         activity_holder_name=f"{john_due.first_name} {john_due.last_name}",
                                         executor=random.randint(min(all_employee_id), max(all_employee_id)),
                                         executor_name="Teresa May",
                                         finish_until=combine_date_time(fake.future_date(), datetime.time(
                                             random.randint(0, 23),
                                             random.randint(0, 59),
                                             random.randint(0, 59))))
        task_entity = TaskActivity(company_id=john_due.company_id,
                                   subject=fake.text(max_nb_chars=10),
                                   describe=fake.text(max_nb_chars=100),
                                   activity_holder=john_due.id,
                                   activity_holder_name=f"{john_due.first_name} {john_due.last_name}",
                                   executor=random.randint(min(all_employee_id), max(all_employee_id)),
                                   executor_name="Mr Andersen",
                                   finish_until=combine_date_time(fake.future_date(), datetime.time(
                                       random.randint(0, 23),
                                       random.randint(0, 59),
                                       random.randint(0, 59))))
        result.extend([call_entity, meeting_entity, task_entity])
    try:
        db.session.add_all(result)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
    return None

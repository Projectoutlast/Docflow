import datetime
import sqlalchemy.exc

from faker import Faker

from web_app.models import Company, Employee
from web_app import db

fake = Faker()

TEST_DATE_WHEN = datetime.date(2024, 12, 31)
TEST_TIME_WHEN = datetime.time(12, 0, 0)


def generate_new_company() -> list:
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
    return result


def generate_new_employee() -> list:
    """
    Generate thirty new employees. Ten employees for each company.
    """
    result = []
    entity = Employee(company_id=453380, first_name="John",  # type: ignore
                       last_name="Due", email="john@example.com", password="123456")  # type: ignore
    entity.generate_password_hash(entity.password)
    result.append(entity)
    for i in range(3):
        for _ in range(10):
            entity = Employee(company_id=453380 + i, first_name=fake.first_name(),  # type: ignore
                              last_name=fake.last_name(), email=fake.email(), password="123456")  # type: ignore
            entity.generate_password_hash(entity.password)
            result.append(entity)
    try:
        db.session.add_all(result)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
    return result

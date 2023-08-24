import pytest

from web_app.models import Company, Employee


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
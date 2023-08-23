import pytest

from web_app import create_app
from web_app.database.models import Company, Employee


@pytest.fixture
def test_client():
    # Set the testing configuration prior to creating Flask application
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client


@pytest.fixture
def new_company():
    company = Company(company_name="Smart", tax_id_number=453380, company_email="smart@example.com")
    return company


@pytest.fixture
def new_employee():
    employee = Employee(
        first_name="Jack", last_name="Sparrow", email="jack@example.com", password="test")  # type: ignore
    employee.generate_password_hash("test")
    return employee

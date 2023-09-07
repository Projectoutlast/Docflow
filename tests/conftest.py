import pytest

from web_app import create_app


@pytest.fixture(scope="module")
def test_client():
    """Create test client instance"""
    # Set the testing configuration prior to creating Flask application
    flask_app = create_app('testing')
    flask_app.config['WTF_CSRF_ENABLED'] = False

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            # Generate test data
            from tests.utils_for_tests import generate_new_company, generate_new_employee

            generate_new_company()
            generate_new_employee()

            yield testing_client


@pytest.fixture(scope="module")
def test_auth_client():
    """Create test client instance"""
    # Set the testing configuration prior to creating Flask application
    flask_app = create_app('testing')
    flask_app.config['WTF_CSRF_ENABLED'] = False

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            # Generate test data
            from tests.utils_for_tests import generate_new_company, generate_new_employee

            generate_new_company()
            generate_new_employee()

            payload = {"email": "john@example.com", "password": "123456"}
            response = testing_client.post("/login", data=payload, follow_redirects=True)
            assert response.status_code == 200
            assert b"Welcome" in response.data

            yield testing_client

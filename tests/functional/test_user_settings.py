import io

from flask_login import current_user

from config import Config
from web_app.models import Company, Employee


def test_show_user_data(test_auth_client):
    """
    GIVEN a Flask application with authentication user
    WHEN the '/user' is requested (GET)
    THEN check that the response is valid / invalid
    """
    response = test_auth_client.get("/user", follow_redirects=True)
    employee = Employee.query.filter(Employee.id == current_user.id).first()
    company = Company.query.filter(Company.id == employee.company_id).first()

    assert response.status_code == 200
    for item in [company.company_name, "Department", "Email", "Change password"]:
        assert bytes(item, "utf-8") in response.data


def test_edit_user_data(test_auth_client):
    """
    GIVEN a Flask application
    WHEN the '/user/edit' is requested (GET)
    THEN check that the responses is valid / invalid, contain correct data and are modified
    """
    response = test_auth_client.get("/user/edit", follow_redirects=True)
    employee = Employee.query.filter(Employee.id == current_user.id).first()

    assert response.status_code == 200
    for item in [employee.first_name, employee.email, "If you change your e-mail, it needs to confirm again.",
                 "Update", "Save changes"]:
        assert bytes(item, "utf-8") in response.data


def test_edit_user_data_process(test_auth_client):
    """
    GIVEN a Flask application
    WHEN the '/user/edit/data' is requested (POST)
    THEN check that the responses is valid / invalid, contain correct data and are modified
    """
    employee = Employee.query.filter(Employee.id == current_user.id).first()
    employee_first_name_before_change = employee.first_name
    employee_last_name_before_change = employee.last_name
    employee_email_before_change = employee.email

    invalid_payload = {"first_name": "Jack", "last_name": "Sparrow"}
    response = test_auth_client.post("/user/edit/data", data=invalid_payload, follow_redirects=True)

    for item in [employee.first_name, employee.last_name, employee.email]:
        assert bytes(item, "utf-8") in response.data

    assert b"Profile successfully updated!" not in response.data

    payload = {"first_name": "Almaz", "last_name": "Andersen", "email": "hack@example.com"}
    response = test_auth_client.post("/user/edit/data", data=payload, follow_redirects=True)
    employee_after_change = Employee.query.filter(Employee.id == current_user.id).first()

    assert response.status_code == 200
    assert b"Profile successfully updated!" in response.data
    assert employee_first_name_before_change != employee_after_change.first_name
    assert employee_last_name_before_change != employee_after_change.last_name
    assert employee_email_before_change != employee_after_change.email
    for item in ["Position", "First name", "Last name", "Email"]:
        assert bytes(item, "utf-8") in response.data


def test_change_user_password(test_auth_client):
    """
    GIVEN a Flask application
    WHEN the '/user/change/password' is requested (GET, POST)
    THEN check that the responses is valid / invalid, form works correct and are modified
    """
    response = test_auth_client.get("/user/change/password", follow_redirects=True)

    assert response.status_code == 200
    for item in ["Current password", "New password", "Confirm new password", "Update"]:
        assert bytes(item, "utf-8") in response.data

    invalid_payload = {"current_password": "12345", "new_password": "123456", "confirm_new_password": "123456"}

    employee = Employee.query.filter(Employee.id == current_user.id).first()
    response = test_auth_client.post("/user/change/password", data=invalid_payload, follow_redirects=True)

    assert b"Incorrect current password" in response.data
    for item in ["Current password", "New password", "Confirm new password", "Update"]:
        assert bytes(item, "utf-8") in response.data

    payload = {"current_password": "123456", "new_password": "1234567", "confirm_new_password": "1234567"}
    response = test_auth_client.post("/user/change/password", data=payload, follow_redirects=True)

    assert response.status_code == 200
    assert b"Password successfully updated!" in response.data
    assert employee.check_password_hash(payload["new_password"]) is True


def test_user_upload_profile_photo(test_auth_client):
    """
    GIVEN a Flask application
    WHEN the '/user/edit/photo' is requested (POST)
    THEN check that the responses is valid / invalid, form works correct, uploaded image file, save it within
    application and save path in database
    """
    file_name = "fake_file_txt.txt"
    invalid_payload = {"photo": (io.BytesIO(b"some initial text data"), file_name)}
    response = test_auth_client.post("/user/edit/photo", data=invalid_payload, follow_redirects=True)

    assert response.status_code == 404

    file_name = "cats.jpeg"
    payload = {"photo": (io.BytesIO(b"some initial text data"), file_name)}
    response = test_auth_client.post("/user/edit/photo", data=payload, follow_redirects=True)
    employee = Employee.query.filter(Employee.id == current_user.id).first()

    assert response.status_code == 200
    assert employee.profile_photo != Config.DEFAULT_AVATAR_PATH

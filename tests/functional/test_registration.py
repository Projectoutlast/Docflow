from web_app.models import Company, Employee


def test_generate_data(test_client):
    """
    GIVEN a Flask application
    WHEN generate data are added (new companies and new employees)
    THEN check that all data were added in test database
    """
    test = Company.query.all()
    assert len(test) > 0


def test_registration_company_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/company' page is requested (GET / POST)
    THEN  check that the response is valid / invalid
    """
    response = test_client.get("/company", follow_redirects=True)
    assert response.status_code == 200
    assert b"Register as company" in response.data
    assert b"Tax identification number" in response.data

    payload = {"name": "Romashka", "tax_id_number": 9996229144, "email": "romashka@example.com"}

    response = test_client.post("/company", data=payload, follow_redirects=True)
    new_company = Company.query.filter(Company.company_email == "romashka@example.com").first()
    assert response.status_code == 200
    assert b"Log in" in response.data
    assert new_company.company_name == "Romashka"

    response = test_client.post("/company", data=payload, follow_redirects=True)
    assert response.status_code != 200

    response = test_client.put("/company")
    assert response.status_code != 200


def test_registration_employee_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/employee' page is requested (GET / POST)
    THEN  check that the response is valid / invalid
    """
    response = test_client.get("/employee", follow_redirects=True)
    assert response.status_code == 200
    assert b"Register as employee" in response.data

    payload = {"first_name": "Jack", "last_name": "Sparrow", "email": "jack@example.com",
               "company_tax_id_number": 453380, "password": "123456", "confirm": "123456"}

    response = test_client.post("/employee", data=payload, follow_redirects=True)
    new_employee = Employee.query.filter(Employee.email == "jack@example.com").first()
    assert response.status_code == 200
    assert b"Log in" in response.data
    assert new_employee.first_name == "Jack"

    response = test_client.post("/employee", data=payload, follow_redirects=True)
    assert response.status_code == 409
    assert b"Register as employee" in response.data

    not_exist_company = {"first_name": "Jack", "last_name": "Sparrow", "email": "jack@example.com",
                         "company_tax_id_number": 324234234, "password": "123456", "confirm": "123456"}

    response = test_client.post("/employee", data=not_exist_company, follow_redirects=True)
    assert response.status_code == 404
    assert b"Register as employee" in response.data

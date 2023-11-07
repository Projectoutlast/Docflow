from web_app.utils.token import confirm_token, generate_token


def test_login(test_client):
    """
    GET a Flask application
    WHEN the '/login' page is requested (GET / POST)
    THEN check that the response is valid / invalid
    """

    response = test_client.get("/login", follow_redirects=True)
    assert response.status_code == 200
    assert b"Log in" in response.data

    invalid_payload = {"email": "qazxswedc@example.com", "password": "234234"}
    valid_payload = {"email": "john@example.com", "password": "123456"}

    response = test_client.post("/login", data=invalid_payload, follow_redirects=True)
    assert response.status_code == 401
    assert b"Log in" in response.data

    response = test_client.post("/login", data=valid_payload, follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome" in response.data

    response = test_client.get("/login", follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome" in response.data

    response = test_client.get("/company", follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome" in response.data

    response = test_client.get("/employee", follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome" in response.data

    response = test_client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Log in" in response.data


def test_unconfirmed_email_user(test_auth_unconfirmed_email_client):
    """
    GET a Flask application
    WHEN the user with an unconfirmed email is logged in
    THEN check that the response is valid / invalid
    """

    response = test_auth_unconfirmed_email_client.get("/unconfirmed-workspace", follow_redirects=True)

    assert response.status_code == 200
    assert b"Your email address has not yet been" in response.data

    response = test_auth_unconfirmed_email_client.get("/workspace", follow_redirects=True)

    assert b"Your email address has not yet been" in response.data


def test_confirmation_token_functionalities(test_auth_unconfirmed_email_client):
    """
    GIVEN a Flask application
    WHEN the register process is going
    THEN check confirmation email functionalities
    """
    payload = {"email": "tom@example.com", "password": "123456"}

    response = test_auth_unconfirmed_email_client.post("/login", data=payload, follow_redirects=True)
    assert response.status_code == 200
    assert b"Hello" in response.data

    invalid_token = generate_token("cat@best.com")
    response = test_auth_unconfirmed_email_client.get(f"/confirm/{invalid_token}", follow_redirects=True)

    assert b"The confirmation link is invalid or has expired." in response.data

    valid_token = generate_token("tom@example.com")
    response = test_auth_unconfirmed_email_client.get(f"/resend", follow_redirects=True)
    assert b"A new confirmation email has been sent." in response.data

    response = test_auth_unconfirmed_email_client.get(f"/confirm/{valid_token}", follow_redirects=True)
    assert b"You have confirmed your account! Thanks" in response.data

    response = test_auth_unconfirmed_email_client.get(f"/confirm/{valid_token}", follow_redirects=True)
    assert b"Account already confirmed." in response.data

    generate_confirm_token_exception = confirm_token(invalid_token, "lalala")
    assert generate_confirm_token_exception is False

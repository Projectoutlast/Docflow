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

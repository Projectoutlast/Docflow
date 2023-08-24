def test_home_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET / POST)
    THEN check that the response is valid / invalid
    """

    response = test_client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Docflow" in response.data
    assert b"Welcome to Docflow" in response.data
    assert b"Managing documents for small business" in response.data

    response = test_client.post("/")
    assert response.status_code == 405
    assert b"Welcome to Docflow" not in response.data

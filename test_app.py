
from app import app


def test_homepage_loads():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Website Uptime Monitor" in response.data


def test_monitoring_form_loads():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Check Website" in response.data


def test_invalid_url():
    client = app.test_client()
    response = client.post("/", data={"url": "not a valid url ://"})

    assert response.status_code == 200
    assert b"Invalid URL" in response.data

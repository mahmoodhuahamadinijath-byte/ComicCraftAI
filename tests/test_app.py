import os

os.environ["MOCK_IMAGES"] = "true"


from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_homepage():

    response = client.get("/")

    assert response.status_code == 200

    assert (
        "Turn your idea into a comic."
        in response.text
    )


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_mock_image():

    response = client.get(
        "/test-image?prompt=test%20fox"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True

    assert data[
        "image_url"
    ].startswith(
        "/static/panels/"
    )

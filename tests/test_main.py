from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_authorize_endpoint():
    response = client.get(
        "/authorize",
        params={
            "client_id": "test_client",
            "response_type": "code",
            "scope": "openid profile",
            "redirect_uri": "https://example.com/callback",
            "state": "test_state",
        },
        follow_redirects=False,
    )
    assert response.status_code == 307
    assert (
        response.headers["location"] == "https://example.com/callback?code=1234567890"
    )

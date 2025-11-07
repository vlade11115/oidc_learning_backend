from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_authorize_endpoint(mocker):
    mocked_code = "1234567890"
    mocker.patch("src.main.new_code", return_value=mocked_code)
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
    location = response.headers["location"]
    assert location.startswith("https://example.com/callback?code=")
    code = location.split("?code=")[1]
    assert code == mocked_code

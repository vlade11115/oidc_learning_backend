from fastapi.testclient import TestClient
import pytest

from src.main import app, check_safe_url


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
    assert response.status_code == 302
    location = response.headers["location"]
    assert location.startswith("https://example.com/callback?code=")
    code = location.split("?code=")[1]
    assert code == mocked_code


def test_check_safe_url(mocker):
    assert check_safe_url("https://example.com") == "https://example.com"
    assert check_safe_url("http://localhost:3000") == "http://localhost:3000"
    with pytest.raises(ValueError):
        assert check_safe_url("http://localhost")
    with pytest.raises(ValueError):
        assert check_safe_url("http://localhost:200")
    with pytest.raises(ValueError):
        assert check_safe_url("/foo")
    with pytest.raises(ValueError):
        assert check_safe_url("http://example.com")

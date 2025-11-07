from fastapi.testclient import TestClient
import pytest
from pydantic import HttpUrl
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
    # TODO: Rewrite this to correctly parse query params
    assert location.startswith("https://example.com/callback?code=")
    assert mocked_code in location
    assert "test_state" in location


@pytest.mark.parametrize(
    "url_string",
    [
        "https://example.com",
        "http://localhost:3000",
    ],
)
def test_check_safe_url_valid_cases(url_string: str):
    """Test that valid URLs pass check_safe_url validation."""
    url = HttpUrl(url_string)
    assert check_safe_url(url) == url


@pytest.mark.parametrize(
    "url_string",
    [
        "http://localhost",
        "http://localhost:200",
        "/foo",
        "http://example.com",
    ],
)
def test_check_safe_url_invalid_cases(url_string: str):
    """Test that invalid URLs raise ValueError in check_safe_url."""
    with pytest.raises(ValueError):
        check_safe_url(HttpUrl(url_string))

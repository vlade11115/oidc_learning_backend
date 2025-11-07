from typing import Annotated, Literal
import uuid

from fastapi import FastAPI, Query
from annotated_types import Len
from fastapi.responses import RedirectResponse
from pydantic import AfterValidator, Field, HttpUrl

from pydantic import BaseModel

from yarl import URL

app = FastAPI()


def check_safe_url(url: HttpUrl):
    """
    Using yarl, check the following:
    1. URL is absolute
    2. URL is HTTPS, if not localhost
    """
    url_to_check = URL(str(url))
    if not url_to_check.absolute:
        raise ValueError("Should be absolute URL")
    if url_to_check.scheme != "https" and url_to_check.host != "localhost":
        raise ValueError("URL should be HTTPS")
    if url_to_check.host == "localhost":
        if not url_to_check.port:
            raise ValueError("localhost URL should explicitly contain port")
        if url_to_check.port < 443:
            raise ValueError("localhost URL port should be more than 443")
    return url


class AuthorizeRequest(BaseModel):
    client_id: str
    response_type: Literal["code"]  # For now, only support authorization code flow
    scope: str | None = None
    redirect_uri: Annotated[
        HttpUrl,
        Len(min_length=1, max_length=2048),
        AfterValidator(check_safe_url),
        Field(
            examples=[
                "http://localhost:8000/callback",
            ],
            description="The redirect URI where the authorization code will be sent. Must be HTTPS (except localhost with port > 443).",
        ),
    ]
    state: str | None = None


def new_code() -> str:
    return str(uuid.uuid4())


@app.get("/authorize", response_class=RedirectResponse, status_code=302)
def authorize_endpoint(request: Annotated[AuthorizeRequest, Query()]):
    code = new_code()
    url = URL(str(request.redirect_uri))
    url = url.with_query({"code": code})
    return str(url)

from typing import Annotated
import uuid

from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse

from pydantic import BaseModel

from yarl import URL

app = FastAPI()


class AuthorizeRequest(BaseModel):
    client_id: str
    response_type: str
    scope: str | None = None
    redirect_uri: str
    state: str | None = None


def new_code() -> str:
    return str(uuid.uuid4())


@app.get("/authorize", response_class=RedirectResponse)
def authorize_endpoint(request: Annotated[AuthorizeRequest, Query()]):
    code = new_code()
    url = URL(request.redirect_uri)
    url = url.with_query({"code": code})
    return str(url)

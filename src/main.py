from typing import Annotated

from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse

from pydantic import BaseModel

app = FastAPI()


class AuthorizeRequest(BaseModel):
    client_id: str
    response_type: str
    scope: str | None = None
    redirect_uri: str
    state: str | None = None


@app.get("/authorize", response_class=RedirectResponse)
def authorize_endpoint(request: Annotated[AuthorizeRequest, Query()]):
    code = "1234567890"
    url = f"{request.redirect_uri}?code={code}"
    return url

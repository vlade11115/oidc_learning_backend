from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()


class AuthorizeRequest(BaseModel):
    client_id: str
    response_type: str
    scope: str
    redirect_uri: str
    state: str


@app.get("/authorize")
def authorize_endpoint(request: Annotated[AuthorizeRequest, Query()]):
    return {
        "client_id": request.client_id,
        "response_type": request.response_type,
        "scope": request.scope,
        "redirect_uri": request.redirect_uri,
        "state": request.state,
    }

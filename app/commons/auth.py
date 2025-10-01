import os
import http

from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException, Depends
from starlette.status import HTTP_401_UNAUTHORIZED

api_key = os.environ["api_key"]

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == api_key:
        return api_key_header
    else:
        status_code = HTTP_401_UNAUTHORIZED
        raise HTTPException(status_code=status_code, detail=http.client.responses[status_code])

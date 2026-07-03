from secrets import compare_digest
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, HTTPBasic, HTTPBasicCredentials

from app.core.config import get_settings

basic_security = HTTPBasic(auto_error=False)
api_key_security = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_hunter(
    credentials: Annotated[HTTPBasicCredentials | None, Depends(basic_security)],
    api_key: Annotated[str | None, Depends(api_key_security)],
) -> str:
    settings = get_settings()
    if api_key and compare_digest(api_key, settings.api_key):
        return "api-key-client"
    if credentials:
        valid_username = compare_digest(credentials.username, settings.demo_username)
        valid_password = compare_digest(credentials.password, settings.demo_password)
        if valid_username and valid_password:
            return credentials.username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid hunter credentials",
        headers={"WWW-Authenticate": "Basic"},
    )

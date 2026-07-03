from secrets import compare_digest
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.core.config import get_settings

security = HTTPBasic()


def require_hunter(credentials: Annotated[HTTPBasicCredentials, Depends(security)]) -> str:
    settings = get_settings()
    valid_username = compare_digest(credentials.username, settings.demo_username)
    valid_password = compare_digest(credentials.password, settings.demo_password)
    if not (valid_username and valid_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid hunter credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

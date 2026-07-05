import secrets

from fastapi import Header, HTTPException, Security, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.core.config import get_settings

basic = HTTPBasic(auto_error=False)


def require_analyst(
    credentials: HTTPBasicCredentials | None = Security(basic),  # noqa: B008
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),  # noqa: B008
) -> str:
    settings = get_settings()
    if x_api_key and secrets.compare_digest(x_api_key, settings.api_key):
        return "api-key"

    if credentials:
        username_ok = secrets.compare_digest(credentials.username, settings.demo_username)
        password_ok = secrets.compare_digest(credentials.password, settings.demo_password)
        if username_ok and password_ok:
            return credentials.username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Valid analyst credentials or X-API-Key header required",
        headers={"WWW-Authenticate": "Basic"},
    )

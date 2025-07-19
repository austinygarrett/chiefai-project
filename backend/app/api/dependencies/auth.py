from collections.abc import Callable

from fastapi import Depends, Request, Security
from fastapi.exceptions import HTTPException
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED

from app.api.dependencies.database import get_repository
from app.core import constant, settings
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.core.token import get_user_from_token
from app.database.repositories.users import UsersRepository
from app.models.user import User

AUTH_HEADER_KEY = settings.auth_header_key


class RWAPIKeyHeader(APIKeyHeader):
    async def __call__(self, request: Request) -> str | None:
        try:
            return await super().__call__(request)
        except HTTPException as auth_exc:
            raise HTTPException(
                status_code=auth_exc.status_code,
                detail=constant.FAIL_AUTH_CHECK,
            )

def get_current_user_auth(
    *,
    required: bool = True,
    cookie_key: str = "token",
) -> Callable:
    async def _get_current_user(
        request: Request,
        settings: AppSettings = Depends(get_app_settings),
        users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    ) -> User | None:
        if (cookie_key not in request.cookies):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail=constant.FAIL_AUTH_INVALID_TOKEN_PREFIX,
            )
       
        token = request.cookies.get(cookie_key)
        
        if not token:
            if required:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Missing access token in cookie.",
                )
            return None

        try:
            secret_key = str(settings.secret_key.get_secret_value())
            token_user = get_user_from_token(token=token, secret_key=secret_key)
        except Exception:
            if required:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Invalid token.",
                )
            return None

        user = await users_repo.get_user_by_email(email=token_user.email)
        if not user:
            if required:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail=constant.FAIL_VALIDATION_MATCHED_USER_EMAIL,
                )
            return None

        return user

    return _get_current_user
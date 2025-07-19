from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.api.dependencies.auth import get_current_user_auth
from app.api.dependencies.database import get_repository
from app.api.dependencies.service import get_service
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.database.repositories.users import UsersRepository
from app.models.user import User
from app.schemas.user import UserInCreate, UserInSignIn, UserResponse
from app.services.users import UsersService
from app.utils import ERROR_RESPONSES, ServiceResult, handle_result

router = APIRouter()


@router.get(
    path="/info",
    status_code=HTTP_200_OK,
    response_model=UserResponse,
    responses=ERROR_RESPONSES,
    name="auth:info",
)
async def get_user_by_token(
    *,
    users_service: UsersService = Depends(get_service(UsersService)),
    token_user: User = Depends(get_current_user_auth()),
) -> ServiceResult:
    """
    Create new users.
    """
    print("token_user", token_user)
    result = await users_service.get_user_by_token(
        token_user=token_user,
    )

    return await handle_result(result)


@router.post(
    path="/login",
    status_code=HTTP_200_OK,
    response_model=UserResponse,
    responses=ERROR_RESPONSES,
    name="auth:login",
)
async def login(
    *,
    users_service: UsersService = Depends(get_service(UsersService)),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    user_in: UserInSignIn,
    settings: AppSettings = Depends(get_app_settings),
) -> ServiceResult:
    """
    Create new users.
    """
    secret_key = str(settings.secret_key.get_secret_value())
    result = await users_service.login_user(users_repo=users_repo, user_in=user_in, secret_key=secret_key)

    response = await handle_result(result)
    
    if result.success:
        response.set_cookie(
            key="token",
            value=result.token,
            httponly=True,
            secure=True,
            samesite="lax",
        )

    return response

@router.post(
    path="/register",
    status_code=HTTP_201_CREATED,
    response_model=UserResponse,
    responses=ERROR_RESPONSES,
    name="auth:register",
)
async def register_user(
    *,
    users_service: UsersService = Depends(get_service(UsersService)),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    user_in: UserInCreate,
    settings: AppSettings = Depends(get_app_settings),
) -> JSONResponse:
    """
    Signup new users and set JWT token in cookie.
    """
    secret_key = str(settings.secret_key.get_secret_value())
    service_result = await users_service.register_user(
        users_repo=users_repo,
        user_in=user_in,
        secret_key=secret_key,
    )

    response = await handle_result(service_result)


    if service_result.success:
        response.set_cookie(
            key="access_token",
            value=service_result.token,
            httponly=True,
            secure=True,
            samesite="lax",
        )

    return response

@router.post(
    path="/logout",
    status_code=HTTP_200_OK,
    name="auth:logout",
)
async def logout(response: Response) -> JSONResponse:
    """
    Logout user by deleting the access token cookie.
    """
    response = JSONResponse(
        content={"message": "Successfully logged out."},
        status_code=HTTP_200_OK,
    )
    response.delete_cookie(
        key="token",
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return response
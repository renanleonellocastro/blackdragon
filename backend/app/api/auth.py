from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.services import auth_service

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(data: RegisterRequest, db: DbSession) -> TokenResponse:
    return await auth_service.register(db, data)


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: DbSession) -> TokenResponse:
    return await auth_service.login(db, data.email, data.password)


@router.post("/refresh")
async def refresh_token(user: CurrentUser, db: DbSession) -> dict[str, str]:
    from fastapi import Request

    # The current user's token is valid; issue a new one
    from app.core.security import create_access_token

    token = create_access_token(user.id, user.tenant_id, user.role.value)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_me(user: CurrentUser) -> UserResponse:
    return UserResponse.model_validate(user)

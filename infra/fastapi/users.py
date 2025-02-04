from __future__ import annotations

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from starlette.responses import JSONResponse

from constants import ERROR_RESPONSES
from core.auth import hash_password, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, oauth2_scheme, \
    decode_token
from core.errors import UserAlreadyExistsError, UserDoesNotExistError
from core.users import User
from infra.fastapi.dependables import UserRepositoryDependable, BlacklistedUserRepositoryDependable

user_api = APIRouter(tags=["Users"])


class RegisterUserRequest(BaseModel):
    username: str
    password: str


class RegisterUserResponse(BaseModel):
    message: str


class RegisterUserResponseEnvelope(BaseModel):
    user: RegisterUserResponse


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginUserResponseEnvelope(BaseModel):
    user: LoginResponse


@user_api.post(
    "/register",
    status_code=201,
    response_model=RegisterUserResponseEnvelope,
    responses={409: ERROR_RESPONSES[409]},
)
def register_user(
        request: RegisterUserRequest, users: UserRepositoryDependable
) -> dict[str, dict[str, str]] | JSONResponse:
    username = request.username
    password = hash_password(request.password)

    user = User(username, password)
    try:
        users.create(user)
        return {"user": {"message": "User registered successfully"}}
    except UserAlreadyExistsError:
        return JSONResponse(
            status_code=409,
            content={
                "error": {"message": f"user with username <{username}>" " already exists."}
            },
        )


@user_api.post(
    "/login",
    status_code=200,
    response_model=LoginUserResponseEnvelope,
    responses={
        401: ERROR_RESPONSES[401],
        404: ERROR_RESPONSES[404]
    },
)
def login_user(
        users: UserRepositoryDependable,
        form_data: OAuth2PasswordRequestForm = Depends()
) -> JSONResponse | dict[str, str | Any]:
    """
    Authenticate user and return JWT access token.
    """
    try:
        user = users.get_by_username(form_data.username)
    except UserDoesNotExistError:
        return JSONResponse(
            status_code=404,
            content={
                "error": {"message": f"User does not exist."}
            },
        )

    if not verify_password(form_data.password, user.password):
        return JSONResponse(
            status_code=401,
            content={
                "error": {"message": f"Invalid username or password."}
            },
        )

    access_token = create_access_token({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"user": {"access_token": access_token, "token_type": "bearer"}}


@user_api.post("/logout", status_code=200)
def logout_user(blacklist: BlacklistedUserRepositoryDependable, token: str = Depends(oauth2_scheme)) -> JSONResponse:
    blacklist.add_token(token)
    return JSONResponse(content={"message": "Logout successful"}, status_code=200)


def get_current_user(users: UserRepositoryDependable, blacklist: BlacklistedUserRepositoryDependable, token: str = Depends(oauth2_scheme)) -> JSONResponse | Any:
    """
    Dependency to get the current logged-in user from the JWT token.
    """
    if blacklist.contains_token(token):
        return JSONResponse(
            status_code=401,
            content={
                "error": {"message": f"Token has been revoked"}
            },
        )

    payload = decode_token(token)  # Decode JWT
    username: str = payload.get("sub")
    if username is None:
        return JSONResponse(
            status_code=401,
            content={
                "error": {"message": f"Invalid authentication token."}
            },
        )

    user = users.get_by_username(username)
    if user is None:
        return JSONResponse(
            status_code=401,
            content={
                "error": {"message": f"Invalid authentication token."}
            },
        )

    return user

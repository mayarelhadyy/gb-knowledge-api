import sqlite3

from fastapi import (
    APIRouter,
    HTTPException
)

from models import (
    RegisterRequest,
    LoginRequest
)

from services.auth_service import (
    create_user,
    authenticate_user,
    create_access_token
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(request: RegisterRequest):

    try:
        user_id = create_user(
            request.email,
            request.password
        )

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    return {
        "message": "User registered successfully",
        "user_id": user_id
    }


@router.post("/login")
def login(request: LoginRequest):

    user = authenticate_user(
        request.email,
        request.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
    user["id"],
    user["role"]
)

    return {
    "access_token": token,
    "token_type": "bearer",
    "role": user["role"]
}
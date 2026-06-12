from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database.session import get_db

from schemas.auth import (
    UserRegister,
    UserLogin
)

from repositories.user_repository import (
    UserRepository
)

from core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from core.dependencies import (
    get_current_user
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    existing_user = (
        UserRepository.get_by_email(
            db,
            user.email
        )
    )

    if existing_user:
        return {
            "message": "Email already registered"
        }

    hashed_password = hash_password(
        user.password
    )

    db_user = (
        UserRepository.create_user(
            db=db,
            email=user.email,
            password_hash=hashed_password
        )
    )

    return {
        "message": "User registered successfully",
        "user_id": db_user.id,
        "email": db_user.email
    }


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = UserRepository.get_by_email(
        db,
        user.email
    )

    if not db_user:
        return {
            "message": "Invalid email or password"
        }

    if not verify_password(
        user.password,
        db_user.password_hash
    ):
        return {
            "message": "Invalid email or password"
        }

    access_token = create_access_token(
        {
            "sub": db_user.id,
            "email": db_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me")
def me(
    current_user=Depends(
        get_current_user
    )
):

    return {
        "user": current_user
    }
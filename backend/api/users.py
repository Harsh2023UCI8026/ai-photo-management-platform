from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database.session import get_db

from repositories.user_repository import UserRepository
from schemas.user import UserCreate


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return UserRepository.create(db, user)


@router.get("/")
def get_users(
    db: Session = Depends(get_db)
):
    return UserRepository.get_all(db)


@router.get("/{user_id}")
def get_user(
    user_id: str,
    db: Session = Depends(get_db)
):

    user = UserRepository.get_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    db: Session = Depends(get_db)
):

    deleted = UserRepository.delete(db, user_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully"
    }
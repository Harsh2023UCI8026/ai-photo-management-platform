from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from database.session import get_db

from core.dependencies import (
    get_current_user
)

from repositories.search_history_repository import (
    SearchHistoryRepository
)

router = APIRouter(
    prefix="/search-history",
    tags=["Search History"]
)


@router.get("/")
def get_search_history(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    history = (
        SearchHistoryRepository.get_by_user(
            db,
            current_user["sub"]
        )
    )

    return history
from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from database.session import (
    get_db
)

from services.collection_service import (
    CollectionService
)

router = APIRouter(
    prefix="/collections",
    tags=["Collections"]
)


@router.get("/")
def get_collections(
    db: Session = Depends(
        get_db
    )
):

    return (
        CollectionService.get_collections(
            db
        )
    )
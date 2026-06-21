from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database.session import get_db

from core.dependencies import (
    get_current_user
)

from repositories.tag_repository import (
    TagRepository
)

from repositories.photo_tag_repository import (
    PhotoTagRepository
)

from repositories.photo_repository import (
    PhotoRepository
)

from models.photo_tag import (
    PhotoTag
)

router = APIRouter(
    prefix="/tags",
    tags=["Tags"]
)


@router.get("/")
def get_tags(
    db: Session = Depends(get_db)
):

    return (
        TagRepository.get_all(db)
    )


@router.post(
    "/photos/{photo_id}"
)
def add_tag(
    photo_id: str,
    tag_name: str,
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):

    photo = (
        PhotoRepository.get_by_id(
            db,
            photo_id
        )
    )

    if not photo:

        raise HTTPException(
            status_code=404,
            detail="Photo not found"
        )

    tag = (
        TagRepository.get_by_name(
            db,
            tag_name
        )
    )

    if not tag:

        tag = (
            TagRepository.create(
                db,
                tag_name
            )
        )

    

    existing = (
        db.query(PhotoTag)
        .filter(
            PhotoTag.photo_id == photo_id,
            PhotoTag.tag_id == tag.id
        )
        .first()
    )

    if existing:

        return {
            "message":
            "Tag already exists"
        }


    return (
        PhotoTagRepository.create(
            db,
            photo_id,
            tag.id
        )
    )


@router.get(
    "/{tag_name}"
)
def get_photos_by_tag(
    tag_name: str,
    db: Session = Depends(
        get_db
    )
):

    tag = (
        TagRepository.get_by_name(
            db,
            tag_name
        )
    )

    if not tag:

        raise HTTPException(
            status_code=404,
            detail="Tag not found"
        )

    relations = (
        PhotoTagRepository.get_by_tag(
            db,
            tag.id
        )
    )

    results = []

    for item in relations:

        photo = (
            PhotoRepository.get_by_id(
                db,
                item.photo_id
            )
        )

        if photo:

            results.append({
                "photo_id":
                photo.id,

                "filename":
                photo.filename
            })

    return results


@router.delete(
    "/photos/{photo_id}/{tag_name}"
)
def remove_tag(
    photo_id: str,
    tag_name: str,
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):
    



    tag = (
        TagRepository.get_by_name(
            db,
            tag_name
        )
    )



    
    if not tag:

        raise HTTPException(
            status_code=404,
            detail="Tag not found"
        )

    PhotoTagRepository.delete(
        db,
        photo_id,
        tag.id
    )

    return {
        "message":
        "Tag removed"
    }
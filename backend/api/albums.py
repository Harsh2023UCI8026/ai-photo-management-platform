from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database.session import get_db

from core.dependencies import (
    get_current_user
)

from schemas.album import (
    AlbumCreate
)

from repositories.album_repository import (
    AlbumRepository
)

from repositories.album_photo_repository import (
    AlbumPhotoRepository
)

from repositories.photo_repository import (
    PhotoRepository
)


router = APIRouter(
    prefix="/albums",
    tags=["Albums"]
)


@router.post("/")
def create_album(
    album: AlbumCreate,
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):

    return (
        AlbumRepository.create(
            db=db,
            user_id=current_user["sub"],
            name=album.name
        )
    )


@router.get("/")
def get_albums(
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):

    return (
        AlbumRepository.get_all(
            db,
            current_user["sub"]
        )
    )


@router.delete(
    "/{album_id}"
)
def delete_album(
    album_id: str,
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):

    album = (
        AlbumRepository.get_by_id(
            db,
            album_id
        )
    )

    if not album:

        raise HTTPException(
            status_code=404,
            detail="Album not found"
        )

    if album.user_id != current_user["sub"]:

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    AlbumRepository.delete(
        db,
        album_id
    )

    return {
        "message":
        "Album deleted"
    }


@router.post(
    "/{album_id}/photos/{photo_id}"
)
def add_photo_to_album(
    album_id: str,
    photo_id: str,
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):

    album = (
        AlbumRepository.get_by_id(
            db,
            album_id
        )
    )

    if not album:

        raise HTTPException(
            status_code=404,
            detail="Album not found"
        )

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

    return (
        AlbumPhotoRepository.add_photo(
            db,
            album_id,
            photo_id
        )
    )


@router.get(
    "/{album_id}"
)
def get_album(
    album_id: str,
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):

    album = (
        AlbumRepository.get_by_id(
            db,
            album_id
        )
    )

    if not album:

        raise HTTPException(
            status_code=404,
            detail="Album not found"
        )

    photos = (
        AlbumPhotoRepository.get_album_photos(
            db,
            album_id
        )
    )

    return {
        "album": album,
        "photos": photos
    }


@router.delete(
    "/{album_id}/photos/{photo_id}"
)
def remove_photo_from_album(
    album_id: str,
    photo_id: str,
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):

    AlbumPhotoRepository.remove_photo(
        db,
        album_id,
        photo_id
    )

    return {
        "message":
        "Photo removed from album"
    }
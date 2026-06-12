from fastapi import HTTPException

from models.photo import Photo


def verify_photo_owner(
    photo: Photo,
    user_id: str
):

    if photo.user_id != user_id:

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )
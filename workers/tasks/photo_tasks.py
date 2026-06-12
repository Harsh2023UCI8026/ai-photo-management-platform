from pathlib import Path

from PIL import Image

from celery_app import celery_app


@celery_app.task
def generate_thumbnail(filename: str):

    uploads_dir = Path("/app/uploads")
    thumbnails_dir = Path("/app/thumbnails")

    thumbnails_dir.mkdir(
        exist_ok=True
    )

    image_path = uploads_dir / filename

    thumbnail_path = (
        thumbnails_dir /
        f"thumb_{filename}"
    )

    with Image.open(image_path) as img:

        img.thumbnail((200, 200))

        img.save(
            thumbnail_path
        )

    return str(thumbnail_path)

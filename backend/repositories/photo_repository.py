from sqlalchemy.orm import Session

from models.photo import Photo
from schemas.photo import PhotoCreate
from services.photo_service import PhotoService


class PhotoRepository:

    @staticmethod
    def create(
        db: Session,
        photo: PhotoCreate
    ):
        db_photo = Photo(
            user_id=photo.user_id,
            filename=photo.filename,
            file_path=photo.file_path,
            thumbnail_path=photo.thumbnail_path,
            file_size=photo.file_size,
            md5_hash=photo.md5_hash,
            sha256_hash=photo.sha256_hash,
            width=photo.width,
            height=photo.height,
            source_type=photo.source_type
        )

        db.add(db_photo)
        db.commit()
        db.refresh(db_photo)

        return db_photo

    @staticmethod
    def create_uploaded_photo(
        db: Session,
        user_id: str,
        filename: str,
        file_path: str,
        thumbnail_path: str,
        file_size: int,
        md5_hash: str,
        sha256_hash: str,
        width: int,
        height: int,
        phash: str,
        dhash: str,
        ahash: str
    ):
        db_photo = Photo(
            user_id=user_id,
            filename=filename,
            file_path=file_path,
            thumbnail_path=thumbnail_path,
            file_size=file_size,
            md5_hash=md5_hash,
            sha256_hash=sha256_hash,
            width=width,
            height=height,
            source_type="upload",
            phash=phash,
            dhash=dhash,
            ahash=ahash
        )

        db.add(db_photo)
        db.commit()
        db.refresh(db_photo)

        return db_photo

    
    @staticmethod
    def get_all(db: Session):
        return (
            db.query(Photo)
            .filter(Photo.is_deleted == False)
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        photo_id: str
    ):
        return (
            db.query(Photo)
            .filter(Photo.id == photo_id)
            .first()
        )

    @staticmethod
    def get_by_sha256(
        db: Session,
        sha256_hash: str
    ):
        return (
            db.query(Photo)
            .filter(Photo.sha256_hash == sha256_hash)
            .first()
        )

    @staticmethod
    def is_duplicate(
        db: Session,
        sha256_hash: str
    ):
        return PhotoRepository.get_by_sha256(
            db,
            sha256_hash
        )

    

    @staticmethod
    def delete(
        db: Session,
        photo_id: str
    ):
        photo = (
            db.query(Photo)
            .filter(Photo.id == photo_id)
            .first()
        )

        if not photo:
            return None

        photo.is_deleted = True

        db.commit()
        db.refresh(photo)

        return photo
    


    @staticmethod
    def permanent_delete(
        db: Session,
        photo_id: str
    ):
        photo = (
            db.query(Photo)
            .filter(Photo.id == photo_id)
            .first()
        )

        if not photo:
            return None

        db.delete(photo)

        db.commit()

        return photo


    
    @staticmethod
    def search_by_filename(
        db: Session,
        filename: str
    ):
        return (
            db.query(Photo)
            .filter(
                Photo.filename.ilike(
                    f"%{filename}%"
                )
            )
            .all()
        )
    

    @staticmethod
    def find_similar_photos(
        db: Session,
        photo_id: str,
        phash: str,
        dhash: str,
        ahash: str,
        threshold: float = 85
    ):

        photos = (
            db.query(Photo)
            .filter(
                Photo.phash.isnot(None),
                Photo.dhash.isnot(None),
                Photo.ahash.isnot(None),
                Photo.is_deleted == False
            )
            .all()
        )

        similar_photos = []

        for photo in photos:

            # Skip same image
            if photo.id == photo_id:
                continue

            similarity = (
                PhotoService.combined_similarity(
                    phash,
                    photo.phash,
                    dhash,
                    photo.dhash,
                    ahash,
                    photo.ahash
                )
            )


            print(
                "SIMILAR CHECK:",
                photo.filename,
                
                similarity
            )

            if similarity >= threshold:

                similar_photos.append({
                    "photo_id": photo.id,
                    "filename": photo.filename,
                    "similarity": similarity
                })

        similar_photos.sort(
            key=lambda x: x["similarity"],
            reverse=True
        )

        return similar_photos
    


    @staticmethod
    def find_most_similar_photo(
        db: Session,
        phash: str,
        dhash: str,
        ahash: str
    ):

        photos = (
            db.query(Photo)
            .filter(
                Photo.phash.isnot(None),
                Photo.dhash.isnot(None),
                Photo.ahash.isnot(None),
                Photo.is_deleted == False
            )
            .all()
        )

        best_match = None
        highest_similarity = 0

        for photo in photos:

            # Skip exact same hash
            if (
                photo.phash == phash
                and
                photo.dhash == dhash
                and
                photo.ahash == ahash
            ):
                continue

            similarity = (
                PhotoService.combined_similarity(
                    phash,
                    photo.phash,
                    dhash,
                    photo.dhash,
                    ahash,
                    photo.ahash
                )
            )

            print(
                "COMPARE:",
                photo.filename,
                similarity
            )

            if similarity > highest_similarity:

                highest_similarity = similarity
                best_match = photo

        return best_match, highest_similarity
    





    @staticmethod
    def count_all(
        db: Session
    ):

        return (
            db.query(Photo)
            .count()
        )
    






    @staticmethod
    def total_storage(
        db: Session
    ):

        photos = (
            db.query(Photo)
            .all()
        )

        return sum(
            photo.file_size or 0
            for photo in photos
        )
    


    @staticmethod
    def add_to_favorites(
        db: Session,
        photo_id: str
    ):

        photo = (
            db.query(Photo)
            .filter(
                Photo.id == photo_id
            )
            .first()
        )

        if not photo:
            return None

        photo.is_favorite = True

        db.commit()

        db.refresh(photo)

        return photo


    @staticmethod
    def remove_from_favorites(
        db: Session,
        photo_id: str
    ):

        photo = (
            db.query(Photo)
            .filter(
                Photo.id == photo_id
            )
            .first()
        )

        if not photo:
            return None

        photo.is_favorite = False

        db.commit()

        db.refresh(photo)

        return photo


     
    @staticmethod
    def count_favorites(
        db: Session
    ):

        return (
            db.query(Photo)
            .filter(
                Photo.is_favorite == True
            )
            .count()
        )


    @staticmethod
    def count_deleted(
        db: Session
    ):

        return (
            db.query(Photo)
            .filter(
                Photo.is_deleted == True
            )
            .count()
        )


    @staticmethod
    def average_file_size(
        db: Session
    ):

        photos = (
            db.query(Photo)
            .filter(
                Photo.is_deleted == False
            )
            .all()
        )

        if not photos:
            return 0

        total = sum(
            photo.file_size
            for photo in photos
        )

        return total / len(photos)
    




    @staticmethod
    def get_favorites(
        db,
        user_id
    ):

        return (
            db.query(Photo)
            .filter(
                Photo.user_id == user_id,
                Photo.is_favorite == True
            )
            .all()
        )


    @staticmethod
    def get_not_deleted(db):

        return (
            db.query(Photo)
            .filter(
            Photo.is_deleted == False,
            Photo.is_archived == False
        )
        .all()
        )
    



    @staticmethod
    def archive_photo(
        db: Session,
        photo_id: str
    ):

        photo = (
            db.query(Photo)
            .filter(
                Photo.id == photo_id
            )
            .first()
        )

        if not photo:
            return None

        photo.is_archived = True

        db.commit()

        db.refresh(photo)

        return photo


    @staticmethod
    def unarchive_photo(
        db: Session,
        photo_id: str
    ):

        photo = (
            db.query(Photo)
            .filter(
                Photo.id == photo_id
            )
            .first()
        )

        if not photo:
            return None

        photo.is_archived = False

        db.commit()

        db.refresh(photo)

        return photo


    @staticmethod
    def get_archived(
        db: Session,
        user_id: str
    ):

        return (
            db.query(Photo)
            .filter(
                Photo.user_id == user_id,
                Photo.is_archived == True
            )
            .all()
        )
    



    @staticmethod
    def get_deleted(
        db: Session,
        user_id: str
    ):

        return (
            db.query(Photo)
            .filter(
                Photo.user_id == user_id,
                Photo.is_deleted == True
            )
            .all()
        )


    @staticmethod
    def restore_photo(
        db: Session,
        photo_id: str
    ):

        photo = (
            db.query(Photo)
            .filter(
                Photo.id == photo_id
            )
            .first()
        )

        if not photo:
            return None

        photo.is_deleted = False

        db.commit()

        db.refresh(photo)

        return photo






 
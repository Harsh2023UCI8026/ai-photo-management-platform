from repositories.photo_repository import (
PhotoRepository
)

from repositories.category_repository import (
CategoryRepository
)

from repositories.face_repository import (
FaceRepository
)

from repositories.face_cluster_repository import (
FaceClusterRepository
)

from repositories.album_repository import (
AlbumRepository
)

from repositories.album_photo_repository import (
AlbumPhotoRepository
)

from repositories.tag_repository import (
TagRepository
)

from repositories.photo_tag_repository import (
PhotoTagRepository
)

class FilterService:

    @staticmethod
    def filter_photos(
        db,
        user_id,
        favorite=None,
        category=None,
        person=None,
        tag=None
    ):

        photos = (
            PhotoRepository.get_not_deleted(
                db
            )
        )

        photos = [
            photo
            for photo in photos
            if str(photo.user_id)
            == str(user_id)
        ]

        
        # FAVORITES
        

        if favorite:

            photos = [
                photo
                for photo in photos
                if photo.is_favorite
            ]

    
        # CATEGORY
    

        if category:

            category_photo_ids = {

                item.photo_id

                for item in (
                    CategoryRepository.get_by_category(
                        db,
                        category
                    )
                )
            }

            photos = [

                photo

                for photo in photos

                if photo.id
                in category_photo_ids
            ]

    
        # PERSON
    

        if person:

            cluster = (
                FaceClusterRepository.get_by_label(
                    db,
                    person
                )
            )

            if not cluster:
                return []

            person_photo_ids = {

                face.photo_id

                for face in (
                    FaceRepository.get_by_cluster(
                        db,
                        cluster.id
                    )
                )
            }

            photos = [

                photo

                for photo in photos

                if photo.id
                in person_photo_ids
            ]

    
        # TAG
    

        if tag:

            tag_obj = (
                TagRepository.get_by_name(
                    db,
                    tag
                )
            )

            if not tag_obj:
                return []

            tag_photo_ids = {

                item.photo_id

                for item in (
                    PhotoTagRepository.get_by_tag(
                        db,
                        tag_obj.id
                    )
                )
            }

            photos = [

                photo

                for photo in photos

                if photo.id
                in tag_photo_ids
            ]
            
        return photos
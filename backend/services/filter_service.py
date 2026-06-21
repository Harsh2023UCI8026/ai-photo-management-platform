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

    #
    # FAVORITES
    #

        if favorite:

            return (
                PhotoRepository.get_favorites(
                    db
                )
            )

    #
    # CATEGORY
    #

        if category:

            categories = (
                CategoryRepository.get_by_category(
                    db,
                    category
                )
            )

            results = []

            for item in categories:

                photo = (
                    PhotoRepository.get_by_id(
                        db,
                        item.photo_id
                    )
                )

                if (
                    photo
                    and str(photo.user_id) == str(user_id)
                ):
                    results.append(photo)

            return results

    #
    # PERSON
    #

        if person:

            cluster = (
                FaceClusterRepository.get_by_label(
                    db,
                    person
                )
            )

            if not cluster:
                return []

            faces = (
                FaceRepository.get_by_cluster(
                    db,
                    cluster.id
                )
            )

            results = []

            added = set()

            for face in faces:

                photo = (
                    PhotoRepository.get_by_id(
                        db,
                        face.photo_id
                    )
                )

                if (
                    photo
                    and photo.id not in added
                    and str(photo.user_id)
                    == str(user_id)
                ):
                    results.append(photo)
                    added.add(photo.id)

            return results
        




        
    # TAG #

        if tag:

            tag_obj = (
                TagRepository.get_by_name(
                    db,
                    tag
                )
            )

            if not tag_obj:
                return []

            photo_tags = (
                PhotoTagRepository.get_by_tag(
                    db,
                    tag_obj.id
                )
            )

            results = []

            for item in photo_tags:

                photo = (
                    PhotoRepository.get_by_id(
                        db,
                        item.photo_id
                    )
                )

                if (
                    photo
                    and str(photo.user_id)
                    == str(user_id)
                ):
                    results.append(photo)

            return results

        return (
            PhotoRepository.get_not_deleted(
                db
            )
        )


from repositories.photo_repository import (
    PhotoRepository
)

from repositories.category_repository import (
    CategoryRepository
)

from repositories.face_repository import (
    FaceRepository
)


class CollectionService:

    @staticmethod
    def get_collections(
        db
    ):

        photos = (
            PhotoRepository.get_not_deleted(
                db
            )
        )

        favorites = len([
            p
            for p in photos
            if p.is_favorite
        ])

        faces = (
            FaceRepository.get_all(
                db
            )
        )

        categories = (
            CategoryRepository.get_all_categories(
                db
            )
        )

        category_counts = {}

        for category in categories:

            name = (
                category.category_name
                .lower()
            )

            category_counts[name] = (
                category_counts.get(
                    name,
                    0
                ) + 1
            )

        collections = [

            {
                "name":
                "favorites",

                "count":
                favorites
            },

            {
                "name":
                "people",

                "count":
                len(faces)
            }
        ]

        for name, count in (
            category_counts.items()
        ):

            collections.append(

                {
                    "name":
                    name,

                    "count":
                    count
                }
            )

        collections.sort(
            key=lambda x: x["count"],
            reverse=True
        )

        return collections
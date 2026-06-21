from repositories.photo_repository import (
    PhotoRepository
)

from repositories.face_repository import (
    FaceRepository
)

from repositories.face_cluster_repository import (
    FaceClusterRepository
)

from repositories.category_repository import (
    CategoryRepository
)


class DashboardService:

    @staticmethod
    def get_stats(
        db
    ):

        return {

            "total_photos":
            PhotoRepository.count_all(
                db
            ),

            "favorite_photos":
            PhotoRepository.count_favorites(
                db
            ),

            "deleted_photos":
            PhotoRepository.count_deleted(
                db
            ),

            "total_storage_bytes":
            PhotoRepository.total_storage(
                db
            ),

            "average_file_size_bytes":
            PhotoRepository.average_file_size(
                db
            ),

            "total_faces":
            FaceRepository.count_faces(
                db
            ),

            "total_clusters":
            FaceClusterRepository.count_clusters(
                db
            ),

            "categories":
            CategoryRepository.get_category_counts(
                db
            )
        }
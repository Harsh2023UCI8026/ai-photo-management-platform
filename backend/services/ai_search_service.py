from repositories.category_repository import (
    CategoryRepository
)

from repositories.photo_ocr_search_repository import (
    PhotoOCRSearchRepository
)

from repositories.photo_repository import (
    PhotoRepository
)

from services.semantic_search_service import (
    SemanticSearchService
)

from services.query_normalizer import (
    QueryNormalizer
)

from repositories.search_history_repository import (
    SearchHistoryRepository
)


class AISearchService:

    @staticmethod
    def search(
        db,
        query,
        user_id
    ):
        
        SearchHistoryRepository.create(
        db=db,
        user_id=user_id,
        query=query
        )

        results = []

        added = set()

        #
        # CATEGORY SEARCH
        #

        normalized_query = (
            QueryNormalizer.normalize(
                query
            )
        )

        categories = (
            CategoryRepository.get_by_category(
                db,
                normalized_query
            )
        )

        for item in categories:

            photo = (
                PhotoRepository.get_by_id(
                    db,
                    item.photo_id
                )
            )

            if (
                photo
                and photo.id not in added
            ):

                results.append({
                    "source": "category",
                    "photo_id": photo.id,
                    "filename": photo.filename
                })

                added.add(photo.id)

        #
        # OCR SEARCH
        #

        ocr_results = (
            PhotoOCRSearchRepository.search(
                db,
                query
            )
        )

        for item in ocr_results:

            photo = (
                PhotoRepository.get_by_id(
                    db,
                    item.photo_id
                )
            )

            if (
                photo
                and photo.id not in added
            ):

                results.append({
                    "source": "ocr",
                    "photo_id": photo.id,
                    "filename": photo.filename
                })

                added.add(photo.id)

        #
        # SEMANTIC SEARCH
        #

        semantic_results = (
            SemanticSearchService.search(
                db=db,
                query=query,
                user_id=user_id,
                limit=20
            )
        )

        for item in semantic_results:

            if (
                item["photo_id"]
                not in added
            ):

                results.append({
                    "source": "semantic",
                    **item
                })

                added.add(
                    item["photo_id"]
                )

        return results
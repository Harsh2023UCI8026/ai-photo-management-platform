from services.ai_search_service import (
    AISearchService
)


class SmartSearchService:

    @staticmethod
    def search(
        db,
        query,
        user_id
    ):

        return (
            AISearchService.search(
                db=db,
                query=query,
                user_id=user_id
            )
        )
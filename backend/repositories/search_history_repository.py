from sqlalchemy.orm import Session

from models.search_history import SearchHistory


class SearchHistoryRepository:

    @staticmethod
    def create(
        db: Session,
        user_id: str,
        query: str
    ):

        search = SearchHistory(
            user_id=user_id,
            query=query
        )

        db.add(search)
        db.commit()
        db.refresh(search)

        return search

    @staticmethod
    def get_by_user(
        db: Session,
        user_id: str
    ):

        return (
            db.query(SearchHistory)
            .filter(
                SearchHistory.user_id == user_id
            )
            .order_by(
                SearchHistory.created_at.desc()
            )
            .all()
        )
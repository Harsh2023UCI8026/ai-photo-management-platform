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
    




    @staticmethod
    def clear_history(
        db: Session,
        user_id: str
    ):

        (
            db.query(SearchHistory)
            .filter(
                SearchHistory.user_id == user_id
            )
            .delete()
        )

        db.commit()


    @staticmethod
    def get_top_queries(
        db: Session,
        user_id: str
    ):

        history = (
            db.query(SearchHistory)
            .filter(
                SearchHistory.user_id == user_id
            )
            .all()
        )

        counts = {}

        for item in history:

            query = item.query.lower()

            counts[query] = (
                counts.get(query, 0)
                + 1
            )

        results = []

        for query, count in counts.items():

            results.append({
                "query": query,
                "count": count
            })

        results.sort(
            key=lambda x: x["count"],
            reverse=True
        )

        return results[:10]
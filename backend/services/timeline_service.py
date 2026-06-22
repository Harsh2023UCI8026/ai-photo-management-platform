from datetime import datetime
from datetime import timedelta

from repositories.photo_repository import (
    PhotoRepository
)


class TimelineService:

    @staticmethod
    def get_summary(
        db,
        user_id
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

        now = datetime.utcnow()

        today = 0
        this_week = 0
        this_month = 0
        older = 0

        for photo in photos:

            if not photo.created_at:
                continue

            age = now - photo.created_at

            if age.days == 0:
                today += 1

            elif age.days <= 7:
                this_week += 1

            elif age.days <= 30:
                this_month += 1

            else:
                older += 1

        return {
            "today": today,
            "this_week": this_week,
            "this_month": this_month,
            "older": older
        }
    




    @staticmethod
    def get_period_photos(
        db,
        user_id,
        period
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

        now = datetime.utcnow()

        results = []

        for photo in photos:

            if not photo.created_at:
                continue

            age = now - photo.created_at

            include = False

            if (
                period == "today"
                and age.days == 0
            ):
                include = True

            elif (
                period == "this_week"
                and age.days <= 7
            ):
                include = True

            elif (
                period == "this_month"
                and age.days <= 30
                and age.days > 7
            ):
                include = True

            elif (
                period == "older"
                and age.days > 30
            ):
                include = True

            if include:

                results.append({
                    "id": photo.id,
                    "filename": photo.filename
                })

        return results
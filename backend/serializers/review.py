from pydantic import BaseModel
from datetime import datetime


class ReviewResponse(BaseModel):
    avatar: str
    userName: str
    date: str
    review: str
    rating: int
    compactAddress: str

    @classmethod
    def from_orm(cls, review):
        """Create ReviewResponse from Review ORM model."""
        avatar = ""
        if review.avatar_asset:
            avatar = review.avatar_asset.url

        date_str = ""
        if review.timestamp:
            review_date = datetime.fromtimestamp(review.timestamp)
            month = review_date.strftime("%B")
            year = review_date.year
            date_str = f"{month} {year}"

        return cls(
            avatar=avatar,
            userName=review.user_name,
            date=date_str,
            review=review.text,
            rating=review.rating,
            compactAddress=review.compact_address,
        )


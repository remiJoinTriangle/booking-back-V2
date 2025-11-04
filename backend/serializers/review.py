from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from datetime import datetime


class ReviewResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    avatar: str
    user_name: str
    date: str
    review: str
    rating: int
    compact_address: str

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
            user_name=review.user_name,
            date=date_str,
            review=review.text,
            rating=review.rating,
            compact_address=review.compact_address,
        )

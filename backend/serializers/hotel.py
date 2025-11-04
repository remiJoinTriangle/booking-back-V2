from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import List, Any, Dict

from .review import ReviewResponse


class HotelResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: int
    name: str
    price: int
    longitude: float
    latitude: float
    thumbnails: List[str]
    vibes: List[str]
    star_rating: float
    comment_aggregated_rating: float
    count_of_comment: int
    flag: Dict[str, Any]
    vibe_flag: Dict[str, Any]
    matching_reason: str
    matching_flag: Dict[str, Any]
    matching_vibe_flag: Dict[str, Any]

    @classmethod
    def from_orm(cls, hotel):
        """Create HotelResponse from Hotel ORM model."""
        return cls(
            id=hotel.id,
            name=hotel.name,
            price=hotel.price,
            longitude=hotel.longitude,
            latitude=hotel.latitude,
            thumbnails=[],  # TODO: Load from assets relationship
            vibes=hotel.vibes.split(",") if hotel.vibes else [],
            star_rating=hotel.star_rating,
            comment_aggregated_rating=hotel.comment_aggregated_rating,
            count_of_comment=0,  # TODO: Count reviews
            flag={},  # TODO: Convert flag to dict
            vibe_flag={},  # TODO: Convert vibe_flag to dict
            matching_reason=f"Experience luxury and comfort at {hotel.name}",
            matching_flag={},  # TODO: Calculate matching flags
            matching_vibe_flag={},  # TODO: Calculate matching vibe flags
        )


class HotelDetailResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: int
    description: str
    name: str
    latitude: float
    longitude: float
    vibes: List[str]
    price: int
    star_rating: float
    comment_aggregated_rating: float
    count_of_comment: int
    comments: List[ReviewResponse]
    highlights: List[Dict[str, Any]]
    date: Dict[str, Any]
    matching_flag: Dict[str, Any]
    matching_vibe_flag: Dict[str, Any]
    matching_reason: str
    start_day: int
    end_day: int
    start_month: int
    end_month: int
    start_year: int
    end_year: int
    images: List[str]
    image_lists: List[str]
    main_image: str
    url: str

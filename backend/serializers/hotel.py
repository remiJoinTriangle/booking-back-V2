from pydantic import BaseModel
from typing import List, Any, Dict

from .review import ReviewResponse


class HotelResponse(BaseModel):
    id: int
    name: str
    price: int
    longitude: float
    latitude: float
    thumbnails: List[str]
    vibes: List[str]
    starRating: float
    commentAggregatedRating: float
    countOfComment: int
    flag: Dict[str, Any]
    vibeFlag: Dict[str, Any]
    matchingReason: str
    matchingFlag: Dict[str, Any]
    matchingVibeFlag: Dict[str, Any]

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
            starRating=hotel.star_rating,
            commentAggregatedRating=hotel.comment_aggregated_rating,
            countOfComment=0,  # TODO: Count reviews
            flag={},  # TODO: Convert flag to dict
            vibeFlag={},  # TODO: Convert vibe_flag to dict
            matchingReason=f"Experience luxury and comfort at {hotel.name}",
            matchingFlag={},  # TODO: Calculate matching flags
            matchingVibeFlag={},  # TODO: Calculate matching vibe flags
        )


class HotelDetailResponse(BaseModel):
    id: int
    description: str
    name: str
    latitude: float
    longitude: float
    vibes: List[str]
    price: int
    starRating: float
    commentAggregatedRating: float
    countOfComment: int
    comments: List[ReviewResponse]
    highlights: List[Dict[str, Any]]
    date: Dict[str, Any]
    matchingFlag: Dict[str, Any]
    matchingVibeFlag: Dict[str, Any]
    matchingReason: str
    startDay: int
    endDay: int
    startMonth: int
    endMonth: int
    startYear: int
    endYear: int
    images: List[str]
    imageLists: List[str]
    mainImage: str
    url: str

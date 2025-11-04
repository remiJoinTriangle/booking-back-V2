from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Optional, List, Any, Dict

from .hotel import HotelResponse


class SessionResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: int
    name: str
    status: int
    longitude: float
    latitude: float
    zoom: int
    last_interacted_in_second: int
    start_day: int
    end_day: int
    start_month: int
    end_month: int
    start_year: int
    end_year: int
    owner_id: int
    flag: Dict[str, Any]
    vibes: List[str]
    price: int
    count_of_room: int
    user_prompt: str
    vibe_flag: Dict[str, Any]
    packed_date: int
    enriched_prompt: str
    initial_min_price: int
    initial_max_price: int
    filter_min_price: int
    filter_max_price: int
    min_star_rating: int
    min_review_rating: float
    number_of_rooms: Optional[List[Dict[str, Any]]] = None

    @classmethod
    def from_orm(cls, session):
        """Create SessionResponse from Session ORM model."""
        return cls(
            id=session.id,
            name=session.name,
            status=session.status,
            longitude=session.longitude,
            latitude=session.latitude,
            zoom=session.zoom,
            last_interacted_in_second=session.last_interacted,
            start_day=session.start_day,
            end_day=session.end_day,
            start_month=session.start_month,
            end_month=session.end_month,
            start_year=session.start_year,
            end_year=session.end_year,
            owner_id=session.owner_id,
            flag={},  # TODO: Convert flag to dict
            vibes=session.vibes.split(",") if session.vibes else [],
            price=session.price,
            count_of_room=session.count_of_room,
            user_prompt=session.user_prompt,
            vibe_flag={},  # TODO: Convert vibe_flag to dict
            packed_date=session.packed_date,
            enriched_prompt=session.enriched_prompt,
            initial_min_price=session.initial_min_price,
            initial_max_price=session.initial_max_price,
            filter_min_price=session.filter_min_price,
            filter_max_price=session.filter_max_price,
            min_star_rating=session.min_star_rating,
            min_review_rating=session.min_review_rating,
            number_of_rooms=session.number_of_rooms,
        )


class SessionWithHotelsResponse(SessionResponse):
    message: Optional[str] = None
    hotels: List[HotelResponse]
    all_vibes: List[str]


class SessionListResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    sessions: List[SessionResponse]


class CreateSessionParameters(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    message: str
    enriched_prompt: str = ""


class AddSessionMessageParameters(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    message: Optional[str] = None


class UpdateSessionDateParameters(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    start_day: int = -1
    end_day: int = -1
    start_month: int = -1
    end_month: int = -1
    start_year: int = -1
    end_year: int = -1
    period: str = ""
    months: Optional[List[Any]] = None


class UpdateSessionFiltersParameters(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    # TODO: use proper amenity/vibe enums/tables
    air_conditioning: bool = False
    airport_shuttle: bool = False
    baby_sitting: bool = False
    balcony_or_terrace: bool = False
    bath: bool = False
    breakfast: bool = False
    child_friendly: bool = False
    concierge: bool = False
    electric_charging_station: bool = False
    fitness_center: bool = False
    kettle_for_tea_or_coffee: bool = False
    kid_club: bool = False
    kitchen_in_room: bool = False
    laundry: bool = False
    parking: bool = False
    pet_allowed: bool = False
    restaurant: bool = False
    room_service: bool = False
    spa: bool = False
    streaming_service: bool = False
    swimming_pool: bool = False
    valet: bool = False
    wifi: bool = False
    adventure: bool = False
    all_inclusive: bool = False
    amazing_view: bool = False
    apart_hotel: bool = False
    atypique: bool = False
    beach_front: bool = False
    bling: bool = False
    business: bool = False
    charming: bool = False
    cultural: bool = False
    family_friendly: bool = False
    foody: bool = False
    hype: bool = False
    lively: bool = False
    luxury: bool = False
    nature: bool = False
    minimalist: bool = False
    mountain: bool = False
    old_money: bool = False
    quiet: bool = False
    romantic: bool = False
    standardized: bool = False
    stylish: bool = False
    super_luxury: bool = False
    villa: bool = False
    wellness: bool = False

    # TODO: use proper null values instead of -1
    price: int = -1
    min_price: int = -1
    max_price: int = -1
    min_star_rating: int = -1
    min_review_rating: int = -1

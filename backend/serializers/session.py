from pydantic import BaseModel
from typing import Optional, List, Any, Dict

from .hotel import HotelResponse


class SessionResponse(BaseModel):
    id: int
    name: str
    status: int
    longitude: float
    latitude: float
    zoom: int
    lastInteractedInSecond: int
    startDay: int
    endDay: int
    startMonth: int
    endMonth: int
    startYear: int
    endYear: int
    ownerId: int
    flag: Dict[str, Any]
    vibes: List[str]
    price: int
    countOfRoom: int
    userPrompt: str
    vibeFlag: Dict[str, Any]
    packedDate: int
    enrichedPrompt: str
    initialMinPrice: int
    initialMaxPrice: int
    filterMinPrice: int
    filterMaxPrice: int
    minStarRating: int
    minReviewRating: float
    numberOfRooms: Optional[List[Dict[str, Any]]] = None

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
            lastInteractedInSecond=session.last_interacted,
            startDay=session.start_day,
            endDay=session.end_day,
            startMonth=session.start_month,
            endMonth=session.end_month,
            startYear=session.start_year,
            endYear=session.end_year,
            ownerId=session.owner_id,
            flag={},  # TODO: Convert flag to dict
            vibes=session.vibes.split(",") if session.vibes else [],
            price=session.price,
            countOfRoom=session.count_of_room,
            userPrompt=session.user_prompt,
            vibeFlag={},  # TODO: Convert vibe_flag to dict
            packedDate=session.packed_date,
            enrichedPrompt=session.enriched_prompt,
            initialMinPrice=session.initial_min_price,
            initialMaxPrice=session.initial_max_price,
            filterMinPrice=session.filter_min_price,
            filterMaxPrice=session.filter_max_price,
            minStarRating=session.min_star_rating,
            minReviewRating=session.min_review_rating,
            numberOfRooms=session.number_of_rooms,
        )


class SessionWithHotelsResponse(SessionResponse):
    message: Optional[str] = None
    hotels: List[HotelResponse]
    allVibes: List[str]


class SessionListResponse(BaseModel):
    sessions: List[SessionResponse]


class CreateSessionParameters(BaseModel):
    message: str
    enrichedPrompt: str = ""


class AddSessionMessageParameters(BaseModel):
    message: Optional[str] = None


class UpdateSessionDateParameters(BaseModel):
    startDay: int = -1
    endDay: int = -1
    startMonth: int = -1
    endMonth: int = -1
    startYear: int = -1
    endYear: int = -1
    period: str = ""
    months: Optional[List[Any]] = None


class UpdateSessionFiltersParameters(BaseModel):
    airConditioning: bool = False
    airportShuttle: bool = False
    babySitting: bool = False
    balconyOrTerrace: bool = False
    bath: bool = False
    breakfast: bool = False
    childFriendly: bool = False
    concierge: bool = False
    electricChargingStation: bool = False
    fitnessCenter: bool = False
    kettleForTeaOrCoffee: bool = False
    kidClub: bool = False
    kitchenInRoom: bool = False
    laundry: bool = False
    parking: bool = False
    petAllowed: bool = False
    restaurant: bool = False
    roomService: bool = False
    spa: bool = False
    streamingService: bool = False
    swimmingPool: bool = False
    valet: bool = False
    wifi: bool = False
    adventure: bool = False
    allInclusive: bool = False
    amazingView: bool = False
    apartHotel: bool = False
    atypique: bool = False
    beachFront: bool = False
    bling: bool = False
    business: bool = False
    charming: bool = False
    cultural: bool = False
    familyFriendly: bool = False
    foody: bool = False
    hype: bool = False
    lively: bool = False
    luxury: bool = False
    nature: bool = False
    minimalist: bool = False
    mountain: bool = False
    oldMoney: bool = False
    quiet: bool = False
    romantic: bool = False
    standardized: bool = False
    stylish: bool = False
    superLuxury: bool = False
    villa: bool = False
    wellness: bool = False
    price: int = -1
    minPrice: int = -1
    maxPrice: int = -1
    minStarRating: int = -1
    minReviewRating: int = -1

from pydantic import BaseModel, confloat
from typing import Optional, List, Any, Dict


# Response models
class ErrorResponse(BaseModel):
    errorMessage: str


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
    number_of_rooms: Optional[Dict[str, Any]] = None


class SessionWithHotelsResponse(SessionResponse):
    message: Optional[str] = None
    hotels: List[HotelResponse]
    allVibes: List[str]


class SessionListResponse(BaseModel):
    sessions: List[SessionResponse]


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
    comments: List[Dict[str, Any]]
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


# Session request models
class HttpPostSessionArguments(BaseModel):
    message: Optional[str] = None
    enrichedPrompt: str = ""


class HttpPostSessionMessageArguments(BaseModel):
    message: Optional[str] = None


class HttpPostSessionMapArguments(BaseModel):
    latitude: confloat(ge=-90.0, le=90.0)
    longitude: confloat(ge=-180.0, le=180.0)
    zoom: int


class HttpPostSessionDateArguments(BaseModel):
    startDay: int = -1
    endDay: int = -1
    startMonth: int = -1
    endMonth: int = -1
    startYear: int = -1
    endYear: int = -1
    period: str = ""
    months: Optional[List[Any]] = None


class HttpPostSessionVibeArguments(BaseModel):
    vibe: str


class HttpPostSessionFiltersArguments(BaseModel):
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


class HttpPostSessionPromptArguments(BaseModel):
    prompt: str

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...serializers import HotelDetailResponse
from ...serializers.review import ReviewResponse
from ...services.session_service import get_session_by_id
from ...services.hotel_service import get_hotel_by_id

router = APIRouter(prefix="/session", tags=["session"])


@router.get("/{session_id}/hotel/{hotel_id}", response_model=HotelDetailResponse)
async def get_session_hotel_detail(
    session_id: int,
    hotel_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    GET /session/{session_id}/hotel/{hotel_id} - Get hotel page for a given session.
    """
    # TODO: Implement authentication
    # TODO: Check session ownership

    # Get session
    session = await get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session [{session_id}] does not exist")

    # Get hotel
    hotel = await get_hotel_by_id(db, hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail=f"Hotel [{hotel_id}] does not exist")

    # Load reviews
    await db.refresh(hotel, ["reviews"])
    reviews = hotel.reviews

    # Load avatar assets for reviews
    # FIXME: remove useless assets table to avoid this join
    for review in reviews:
        await db.refresh(review, ["avatar_asset"])

    # Format reviews using serializer
    formatted_reviews = [ReviewResponse.from_orm(review) for review in reviews]

    # Load hotel assets
    # FIXME: remove useless assets table to avoid this join
    await db.refresh(hotel, ["assets"])
    hotel_assets = hotel.assets

    # Format images
    all_images = []
    for join_asset in hotel_assets:
        await db.refresh(join_asset, ["asset"])
        if join_asset.asset:
            url = join_asset.asset.url
            all_images.append(url)

    # Get main image
    await db.refresh(hotel, ["main_image_asset"])
    main_image = hotel.main_image_asset.url if hotel.main_image_asset else ""

    # TODO: Store vibes in a dedicated table and retrieve them here
    vibes = hotel.vibes.split(",") if hotel.vibes else []

    # TODO: Calculate matching flags (= amenities) and vibe flags (= vibes) once they are stored in dedicated tables
    # TODO: Format date properly from session

    return HotelDetailResponse(
        id=hotel.id,
        description=hotel.description,
        name=hotel.name,
        latitude=hotel.latitude,
        longitude=hotel.longitude,
        vibes=vibes,
        price=hotel.price,
        starRating=hotel.star_rating,
        commentAggregatedRating=hotel.comment_aggregated_rating,
        countOfComment=len(formatted_reviews),
        comments=formatted_reviews,
        highlights=[],  # TODO: Format highlights
        date={},  # TODO: Format date from session
        matchingFlag={},  # TODO: Calculate matching flags
        matchingVibeFlag={},  # TODO: Calculate matching vibe flags
        matchingReason=f"Experience luxury and comfort at {hotel.name}",
        startDay=session.start_day,
        endDay=session.end_day,
        startMonth=session.start_month,
        endMonth=session.end_month,
        startYear=session.start_year,
        endYear=session.end_year,
        images=all_images,
        imageLists=[],  # TODO: Format image lists
        mainImage=main_image,
        url=hotel.url,
    )

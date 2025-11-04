from sqlalchemy import (
    BigInteger,
    SmallInteger,
    Integer,
    Text,
    Boolean,
    Float,
    Double,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column


class AstraBase(DeclarativeBase):
    # FIXME add common columns here
    pass


# --- Core Tables ---


class Asset(AstraBase):
    __tablename__ = "asset"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(Text, index=True, unique=True, nullable=False)

    # Relationships
    activities = relationship("Activity", back_populates="icon_asset")
    amenities = relationship("Amenity", back_populates="icon_asset")
    food_habits = relationship("FoodHabit", back_populates="icon_asset")
    sports = relationship("Sport", back_populates="icon_asset")
    reviews = relationship("Review", back_populates="avatar_asset")
    users = relationship("User", back_populates="avatar_asset")
    hotels = relationship("Hotel", back_populates="main_image_asset")
    prompt_amenities = relationship("PromptAmenity", back_populates="asset")


class Activity(AstraBase):
    __tablename__ = "activity"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(Text, default="")
    icon_asset_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("asset.id"))
    icon_asset = relationship("Asset", back_populates="activities")
    displayable: Mapped[bool] = mapped_column(Boolean, default=True)

    users = relationship(
        "User", secondary="join_user_activity", back_populates="activities"
    )


class Amenity(AstraBase):
    __tablename__ = "amenity"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(Text, default="")
    icon_asset_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("asset.id"))
    icon_asset = relationship("Asset", back_populates="amenities")
    displayable: Mapped[bool] = mapped_column(Boolean, default=True)

    users = relationship(
        "User", secondary="join_user_amenity", back_populates="amenities"
    )


class FoodHabit(AstraBase):
    __tablename__ = "food_habit"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(Text, default="")
    icon_asset_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("asset.id"))
    icon_asset = relationship("Asset", back_populates="food_habits")

    displayable: Mapped[bool] = mapped_column(Boolean, default=True)

    users = relationship(
        "User", secondary="join_user_food_habit", back_populates="food_habits"
    )


class Sport(AstraBase):
    __tablename__ = "sport"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(Text, default="")
    icon_asset_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("asset.id"))
    icon_asset = relationship("Asset", back_populates="sports")
    displayable: Mapped[bool] = mapped_column(Boolean, default=True)

    users = relationship("User", secondary="join_user_sport", back_populates="sports")


class HotelImageCategory(AstraBase):
    __tablename__ = "hotel_image_category"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(Text, default="")

    join_assets = relationship("JoinHotelAsset", back_populates="category")


class Review(AstraBase):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    avatar_asset_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("asset.id"))
    user_name: Mapped[str] = mapped_column(Text, default="")
    timestamp: Mapped[int] = mapped_column(BigInteger, default=0)
    text: Mapped[str] = mapped_column(Text, default="")
    compact_address: Mapped[str] = mapped_column(Text, default="Dunkirk, Fr")
    rating: Mapped[int] = mapped_column(SmallInteger, default=4)

    avatar_asset = relationship("Asset", back_populates="reviews")
    hotels = relationship(
        "Hotel", secondary="join_hotel_review", back_populates="reviews"
    )


class Hotel(AstraBase):
    __tablename__ = "hotel"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(Text, default="")
    latitude: Mapped[float] = mapped_column(Double, default=0)  # FIXME
    longitude: Mapped[float] = mapped_column(Double, default=0)  # FIXME
    price: Mapped[int] = mapped_column(SmallInteger, default=-1)  # FIXME
    vibes: Mapped[str] = mapped_column(Text, default="")
    internal_rating: Mapped[int] = mapped_column(SmallInteger, default=0)  # FIXME
    description: Mapped[str] = mapped_column(Text, default="")
    star_rating: Mapped[float] = mapped_column(Float, default=4.0)  # FIXME
    main_image_asset_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("asset.id"))
    main_image_asset = relationship("Asset", back_populates="hotels")
    url: Mapped[str] = mapped_column(Text)
    flag: Mapped[int] = mapped_column(BigInteger, default=0)  # FIXME
    vibe_flag: Mapped[int] = mapped_column(BigInteger, default=0)  # FIXME
    comment_aggregated_rating: Mapped[float] = mapped_column(Float, default=4.69)
    number_of_rooms: Mapped[int] = mapped_column(Integer, default=-1)  # FIXME

    assets = relationship("JoinHotelAsset", back_populates="hotel")
    reviews = relationship(
        "Review", secondary="join_hotel_review", back_populates="hotels"
    )


class Example(AstraBase):
    __tablename__ = "example"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    thumbnail: Mapped[str] = mapped_column(Text)
    text: Mapped[str] = mapped_column(Text)
    preview: Mapped[str] = mapped_column(Text)
    prompt: Mapped[str] = mapped_column(Text)
    thumbnailblurhash: Mapped[str] = mapped_column(Text)
    previewblurhash: Mapped[str] = mapped_column(Text)
    displayable: Mapped[bool] = mapped_column(Boolean, default=True)


class PromptAmenity(AstraBase):
    __tablename__ = "prompt_amenity"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(Text, default="")
    sub_title: Mapped[str] = mapped_column(Text, default="")
    asset_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("asset.id"))
    asset = relationship("Asset", back_populates="prompt_amenities")
    displayable: Mapped[bool] = mapped_column(Boolean, default=True)


class Message(AstraBase):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    type: Mapped[int] = mapped_column(SmallInteger)
    text: Mapped[str] = mapped_column(Text)
    function_name: Mapped[str] = mapped_column(Text, default="")
    function_argument_string: Mapped[str] = mapped_column(Text, default="")
    tool_id: Mapped[str] = mapped_column(Text, default="")

    sessions = relationship(
        "Session", secondary="join_session_message", back_populates="messages"
    )


class Session(AstraBase):
    __tablename__ = "session"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    status: Mapped[int] = mapped_column(SmallInteger)
    longitude: Mapped[float] = mapped_column(Double)
    latitude: Mapped[float] = mapped_column(Double)
    zoom: Mapped[int] = mapped_column(SmallInteger)
    last_interacted: Mapped[int] = mapped_column(BigInteger)
    start_day: Mapped[int] = mapped_column(SmallInteger, default=1)
    end_day: Mapped[int] = mapped_column(SmallInteger, default=1)
    start_month: Mapped[int] = mapped_column(SmallInteger, default=1)
    end_month: Mapped[int] = mapped_column(SmallInteger, default=1)
    start_year: Mapped[int] = mapped_column(SmallInteger, default=1970)
    end_year: Mapped[int] = mapped_column(SmallInteger, default=1970)
    owner_id: Mapped[int] = mapped_column(BigInteger, default=-1)
    flag: Mapped[int] = mapped_column(BigInteger, default=0)
    vibes: Mapped[str] = mapped_column(Text, default="")
    price: Mapped[int] = mapped_column(SmallInteger, default=-1)
    count_of_room: Mapped[int] = mapped_column(SmallInteger, default=-1)
    user_prompt: Mapped[str] = mapped_column(Text, default="")
    vibe_flag: Mapped[int] = mapped_column(BigInteger, default=0)
    packed_date: Mapped[int] = mapped_column(BigInteger, default=0)
    enriched_prompt: Mapped[str] = mapped_column(Text, default="")
    initial_min_price: Mapped[int] = mapped_column(SmallInteger, default=-1)
    initial_max_price: Mapped[int] = mapped_column(SmallInteger, default=-1)
    filter_min_price: Mapped[int] = mapped_column(SmallInteger, default=-1)
    filter_max_price: Mapped[int] = mapped_column(SmallInteger, default=-1)
    min_star_rating: Mapped[int] = mapped_column(SmallInteger, default=-1)
    min_review_rating: Mapped[float] = mapped_column(Float, default=-1.0)
    number_of_rooms: Mapped[dict] = mapped_column(JSON)

    messages = relationship(
        "Message", secondary="join_session_message", back_populates="sessions"
    )
    users = relationship(
        "User", secondary="join_user_session", back_populates="sessions"
    )  # FIXME


class User(AstraBase):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text)
    last_name: Mapped[str] = mapped_column(Text, default="")
    age: Mapped[int] = mapped_column(SmallInteger, nullable=True)  # FIXME
    account_created_at: Mapped[int] = mapped_column(BigInteger, default=0)
    phone_number: Mapped[str] = mapped_column(Text, default="")
    preferred_price_per_night: Mapped[int] = mapped_column(SmallInteger, default=3)
    recurrence_of_stay: Mapped[int] = mapped_column(SmallInteger, default=3)
    business_or_leisure: Mapped[int] = mapped_column(SmallInteger, default=3)
    hotel_or_villa: Mapped[int] = mapped_column(SmallInteger, default=3)
    token_hash: Mapped[int] = mapped_column(BigInteger, unique=True, default=0)
    avatar_asset_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("asset.id"))

    avatar_asset = relationship("Asset", back_populates="users")
    activities = relationship(
        "Activity", secondary="join_user_activity", back_populates="users"
    )
    amenities = relationship(
        "Amenity", secondary="join_user_amenity", back_populates="users"
    )
    food_habits = relationship(
        "FoodHabit", secondary="join_user_food_habit", back_populates="users"
    )
    sports = relationship("Sport", secondary="join_user_sport", back_populates="users")
    sessions = relationship(
        "Session", secondary="join_user_session", back_populates="users"
    )


# --- Join Tables ---


class JoinHotelAsset(AstraBase):
    __tablename__ = "join_hotel_asset"

    hotel_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("hotel.id"), primary_key=True
    )
    asset_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("asset.id"), primary_key=True
    )
    category_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("hotel_image_category.id"), default=-2
    )

    hotel = relationship("Hotel", back_populates="assets")
    category = relationship("HotelImageCategory", back_populates="join_assets")
    asset = relationship("Asset")


class JoinHotelReview(AstraBase):
    __tablename__ = "join_hotel_review"

    hotel_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("hotel.id"), primary_key=True
    )
    review_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("review.id"), primary_key=True
    )


class JoinSessionMessage(AstraBase):
    __tablename__ = "join_session_message"

    session_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("session.id"), primary_key=True
    )
    message_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("message.id"), primary_key=True
    )


class JoinUserActivity(AstraBase):
    __tablename__ = "join_user_activity"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id"), primary_key=True
    )
    activity_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("activity.id"), primary_key=True
    )


class JoinUserAmenity(AstraBase):
    __tablename__ = "join_user_amenity"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id"), primary_key=True
    )
    amenity_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("amenity.id"), primary_key=True
    )


class JoinUserFoodHabit(AstraBase):
    __tablename__ = "join_user_food_habit"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id"), primary_key=True
    )
    food_habit_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("food_habit.id"), primary_key=True
    )


class JoinUserSession(AstraBase):
    __tablename__ = "join_user_session"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id"), primary_key=True
    )
    session_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("session.id"), primary_key=True
    )


class JoinUserSport(AstraBase):
    __tablename__ = "join_user_sport"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id"), primary_key=True
    )
    sport_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("sport.id"), primary_key=True
    )

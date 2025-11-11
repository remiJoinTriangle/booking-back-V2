from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class UserSerializer(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    id: Optional[int] = None
    name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    account_created_at: Optional[int] = None
    phone_number: Optional[str] = None
    preferred_price_per_night: Optional[int] = None
    recurrence_of_stay: Optional[int] = None
    business_or_leisure: Optional[int] = None
    hotel_or_villa: Optional[int] = None
    token_hash: Optional[int] = None
    avatar_asset_id: Optional[int] = None
    auth0_id: Optional[str] = None


class CreateUserSerializer(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    account_created_at: Optional[int] = None
    phone_number: Optional[str] = None
    preferred_price_per_night: Optional[int] = None
    recurrence_of_stay: Optional[int] = None
    business_or_leisure: Optional[int] = None
    hotel_or_villa: Optional[int] = None
    token_hash: Optional[int] = None
    avatar_asset_id: Optional[int] = None


class UpdateUserSerializer(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    account_created_at: Optional[int] = None
    phone_number: Optional[str] = None
    preferred_price_per_night: Optional[int] = None
    recurrence_of_stay: Optional[int] = None
    business_or_leisure: Optional[int] = None
    hotel_or_villa: Optional[int] = None
    token_hash: Optional[int] = None
    avatar_asset_id: Optional[int] = None

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models import User
from backend.serializers.user import (
    CreateUserSerializer,
    UpdateUserSerializer,
    UserSerializer,
)
from backend.services.user_service import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


@router.get("", response_model=UserSerializer)
async def get_me(
    user_data=Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    auth0_id = user_data.get("auth0_id")
    if auth0_id is None:
        raise HTTPException(status_code=404, detail="User not found.")
    result = await db.execute(select(User).where(User.auth0_id == auth0_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return UserSerializer.model_validate(user)


@router.put("/update", response_model=UserSerializer)
async def update_user(
    user_data=Depends(get_current_user),
    user_update: UpdateUserSerializer = Body(...),
    db: AsyncSession = Depends(get_db),
):
    user = user_data.get("user")
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    update_values = user_update.model_dump(exclude_unset=True)
    for field, value in update_values.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return UserSerializer.model_validate(user)


@router.delete("/delete", response_model=dict)
async def delete_user(
    user_data=Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    user = user_data.get("user")
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    await db.delete(user)
    await db.commit()
    return {"message": "User deleted successfully."}


@router.post("/create", response_model=UserSerializer)
async def create_user(
    user_data=Depends(get_current_user),
    user_create: CreateUserSerializer = Body(...),
    db: AsyncSession = Depends(get_db),
):
    auth0_id = user_data.get("auth0_id")
    result = await db.execute(select(User).where(User.auth0_id == auth0_id))
    user = result.scalar_one_or_none()
    if user is not None:
        raise HTTPException(status_code=400, detail="User already exists.")
    user = User(
        auth0_id=auth0_id,
        name=user_create.name,
        last_name=user_create.last_name,
        age=user_create.age,
        account_created_at=user_create.account_created_at,
        phone_number=user_create.phone_number,
        preferred_price_per_night=user_create.preferred_price_per_night,
        recurrence_of_stay=user_create.recurrence_of_stay,
        business_or_leisure=user_create.business_or_leisure,
        hotel_or_villa=user_create.hotel_or_villa,
        token_hash=user_create.token_hash,
        avatar_asset_id=user_create.avatar_asset_id,
    )
    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return UserSerializer.model_validate(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/avatar", response_model=UserSerializer)
async def set_avatar(
    user_data=Depends(get_current_user),
    avatar_asset_id: int = Body(...),
    db: AsyncSession = Depends(get_db),
):
    user = user_data.get("user")
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    user.avatar_asset_id = avatar_asset_id
    await db.commit()
    await db.refresh(user)
    return UserSerializer.model_validate(user)

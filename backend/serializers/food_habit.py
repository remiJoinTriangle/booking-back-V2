from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class FoodHabitResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    id: int
    name: str
    icon_asset_id: int
    displayable: bool

    @classmethod
    def from_orm(cls, food_habit):
        return cls(
            id=food_habit.id,
            name=food_habit.name,
            icon_asset_id=food_habit.icon_asset_id,
            displayable=food_habit.displayable,
        )

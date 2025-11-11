from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ActivityResponse(BaseModel):
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
    def from_orm(cls, activity):
        return cls(
            id=activity.id,
            name=activity.name,
            icon_asset_id=activity.icon_asset_id,
            displayable=activity.displayable,
        )

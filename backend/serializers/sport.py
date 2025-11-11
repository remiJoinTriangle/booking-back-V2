from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class SportResponse(BaseModel):
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
    def from_orm(cls, sport):
        return cls(
            id=sport.id,
            name=sport.name,
            icon_asset_id=sport.icon_asset_id,
            displayable=sport.displayable,
        )


from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class AmenityResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: int
    name: str
    icon_asset_id: int
    displayable: bool

    @classmethod
    def from_orm(cls, amenity):
        return cls(
            id=amenity.id,
            name=amenity.name,
            icon_asset_id=amenity.icon_asset_id,
            displayable=amenity.displayable,
        )

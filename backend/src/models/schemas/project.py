import datetime
from typing import Annotated, Optional

from annotated_types import Len
from pydantic import BaseModel, model_validator


class Geometry(BaseModel):
    type: str
    coordinates: list[
        list[list[Annotated[list[float], Len(min_length=2, max_length=2)]]]
    ]


class GeoFile(BaseModel):
    type: str
    geometry: Geometry


class CreateProjectSchema(BaseModel):
    name: str
    description: Optional[str] = ""
    date_range_from: datetime.datetime
    date_range_to: datetime.datetime
    geo_file: GeoFile

    @model_validator(mode="after")
    def check_field_relationship(cls, model):
        if model.date_range_to < model.date_range_from:
            raise ValueError("date_range_to cannot be smaller than date_range_from")
        return model


class UpdateProjectSchema(CreateProjectSchema): ...


class ResponseProjectSchema(CreateProjectSchema):
    id: int

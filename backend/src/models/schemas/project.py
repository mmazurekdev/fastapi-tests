import datetime
from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel


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
    description: str
    date_range_from: datetime.datetime
    date_range_to: datetime.datetime
    geo_file: GeoFile


class UpdateProjectSchema(CreateProjectSchema): ...


class ResponseProjectSchema(CreateProjectSchema):
    id: int

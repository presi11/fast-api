from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.fields import Field


class BaseDog(BaseModel):
    name: str = Field(...)
    description: Optional[str] = Field("")
    picture: Optional[str] = Field("")
    is_adopted: bool = Field(False)

class CreateDog(BaseDog):
    pass


class UpdateDog(BaseModel):
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)


class SearchDog(BaseModel):
    name__icontains: Optional[str] = Field(None, alias="name")
    description__icontains: Optional[str] = Field(None, alias="description")

    class Config:
        allow_population_by_field_name = True


class DogInDB(BaseDog):
    id: int = Field(...)
    created_at: datetime = Field(...)


class Dog(DogInDB):
    class Config:
        orm_mode = True
from datetime import datetime
from typing import Any, Optional, TypeVar

from pydantic import BaseModel, Field
from tortoise.models import Model

ModelType = TypeVar("ModelType", bound=Model)

CrudType = TypeVar("CrudType", bound=Any)

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CountDB(BaseModel):
    count: int = Field(...)


class RangeDates(BaseModel):
    initial_date: Optional[datetime] = Field(None)
    final_date: Optional[datetime] = Field(None)

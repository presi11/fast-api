from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Union
from uuid import UUID

from app.schemas.general import CreateSchemaType, ModelType, UpdateSchemaType


class IServiceBase(Generic[CreateSchemaType, UpdateSchemaType], ABC):  # type: ignore
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self, *, id: Union[int, str, UUID], obj_in: Dict[str, Any]
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *, id: Union[int, str, UUID]) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_byid(self, *, id: Union[int, str, UUID]) -> Optional[ModelType]:
        raise NotImplementedError

    @abstractmethod
    async def get_all(
        self,
        *,
        payload: Dict[str, Any],
        skip: int,
        limit: int,
        order_by: Optional[str] = None,
        date_range: Optional[Dict[str, datetime]] = None,
    ) -> List[ModelType]:
        raise NotImplementedError

    @abstractmethod
    async def count(
        self,
        *,
        payload: Dict[str, Any],
        date_range: Optional[Dict[str, datetime]] = None,
        status__in: Optional[List[str]] = None,
    ) -> int:
        raise NotImplementedError

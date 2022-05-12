from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from app.infra.services.base import IServiceBase
from app.schemas.general import CreateSchemaType, CrudType, ModelType, UpdateSchemaType


class BaseService(IServiceBase[CreateSchemaType, UpdateSchemaType]):
    def __init__(self, crud: CrudType):
        self._queries = crud

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        new_obj = await self._queries.create(obj_in=obj_in)
        return new_obj

    async def get_byid(self, id: Union[int, str, UUID]) -> Optional[ModelType]:
        obj_found = await self._queries.get_byid(id=id)
        if obj_found:
            return obj_found
        return None

    async def get_all(
        self,
        *,
        payload: Dict[str, Any],
        skip: int,
        limit: int,
        order_by: Optional[str] = None,
        date_range: Optional[Dict[str, datetime]] = None,
    ) -> List[ModelType]:
        objs_found = await self._queries.get_all(
            payload=payload,
            skip=skip,
            limit=limit,
            order_by=order_by,
            date_range=date_range,
        )
        return objs_found

    async def update(self, id: Union[int, str, UUID], obj_in: UpdateSchemaType) -> bool:
        payload = obj_in.dict(exclude_unset=True)
        obj_updated = await self._queries.update(id=id, obj_in=payload)
        return obj_updated

    async def delete(self, id: Union[int, str, UUID]) -> int:
        obj_removed = await self._queries.delete(id=id)
        return obj_removed

    async def count(
        self,
        *,
        payload: Dict[str, Any] = {},
        date_range: Optional[Dict[str, datetime]] = None,
        status__in: Optional[List[str]] = None,
    ) -> int:
        if "user_id" in payload and payload["user_id"] == -1:
            payload["user_id"] = None
        if status__in is not None:
            payload["status__in"] = status__in
        count = await self._queries.count(payload=payload, date_range=date_range)
        return count

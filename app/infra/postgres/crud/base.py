from datetime import datetime
from typing import Any, Dict, Generic, List, Optional

from app.schemas.general import CreateSchemaType, ModelType, UpdateSchemaType


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):  # type: ignore
    def __init__(self, *, model: ModelType) -> None:
        self.model = model

    async def get_all(
        self,
        *,
        payload: Dict[str, Any] = {},
        skip: int = 0,
        limit: int = 10,
        order_by: Optional[str] = None,
        date_range: Optional[Dict[str, datetime]] = None,
    ) -> List[ModelType]:
        query = self.model.filter(**payload).all().offset(skip).limit(limit)
        if order_by is not None:
            query = query.order_by(order_by)
        if date_range is not None:
            query = query.filter(
                created_at__range=(date_range["initial_date"], date_range["final_date"])
            )
        model = await query
        return model

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        model = await self.model.create(**obj_in.dict())
        return model
    

    async def update(self, *, id: int, obj_in: Dict[str, Any]) -> bool:
        model = await self.model.get(id=id)
        await model.update_from_dict(obj_in).save()
        return True

    async def delete(self, *, id: int) -> int:
        delete = await self.model.get(id=id).delete()
        return delete

    async def get_byid(self, *, id: int) -> Optional[ModelType]:
        model = await self.model.get_or_none(id=id)
        return model

    async def count(
        self,
        *,
        payload: Dict[str, Any] = {},
        date_range: Optional[Dict[str, datetime]] = None,
    ) -> int:
        query = self.model.filter(**payload)
        if date_range is not None:
            query = query.filter(
                created_at__range=(date_range["initial_date"], date_range["final_date"])
            )
        count = await query.all().count()
        return count

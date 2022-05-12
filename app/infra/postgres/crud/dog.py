from app.infra.postgres.crud.base import CRUDBase
from app.infra.postgres.models.dog import Dog
from app.schemas.dog import CreateDog, UpdateDog


class CRUDDog(CRUDBase[Dog, CreateDog, UpdateDog]):
    ...

crud_dog = CRUDDog(model=Dog)

from app.infra.postgres.crud.dog import crud_dog
from app.infra.postgres.models.dog import Dog
from app.infra.services.base_service import BaseService
from app.schemas.dog import CreateDog
import requests
from app.core.celery import celery_app

class ServiceDog(BaseService):
    async def create(self, *, obj_in: CreateDog) -> Dog  :
        URL='https://dog.ceo/api/breeds/image/random'
        data = requests.get(URL) 
        data = data.json()
        obj_in.picture = data["message"]
        new_obj = await self._queries.create(obj_in=obj_in)
        celery_app.send_task(
        "app.worker.task.task",
        args=[5],
        queue="some-function",
        ) 
        return new_obj



dog_service = ServiceDog(crud=crud_dog)
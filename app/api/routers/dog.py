from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from fastapi.responses import JSONResponse, Response

from app.schemas.dog import Dog, CreateDog, SearchDog, UpdateDog
from app.schemas.general import CountDB
from app.services.dog import dog_service

router = APIRouter()


@router.get(
    "",
    response_class=JSONResponse,
    response_model=List[Dog],
    status_code=200,
    responses={
        200: {"description": "Dogs found"},
    },
)
async def get_all(
    skip: int = Query(0),
    limit: int = Query(10),
    search: SearchDog = Depends(SearchDog),
):
    """
    Obtain dog that satisfy the parameters entered.
    **Args**:
    - **Headers**:
        - accept: application/json
    - **Query Params**:
        - **skip** (int, optional): total data to be omitted.
        - **limit** (int, optional): total data to be searched.
        - **name** (str, optional): name of the dog.
        - **description** (str, optional): description of the dog.
    **Returns**:
    - **200** (Optional[List[JSON]]):
        - **name** (str, optional): name of the dog.
        - **description** (str, optional): description of the dog.
        - **id** (int): Database id corresponding to the dog.
        - **created_at** (datetime): Date of creation of the dog in the database (UTC time)
        - **last_modified** (datetime): Date of the last modification of the dog in the database (UTC time)
    - **400** (JSON): Bad Request
    - **401** (JSON): The user doesn't have enough privileges
    - **422** (JSON): Unprocessable Entity
    - **500** (JSON): Internal Server Error (Please, contact administrators)
    """
    dogs = await dog_service.get_all(
        skip=skip, limit=limit, payload=search.dict(exclude_none=True)
    )
    return dogs


@router.get(
    "/count",
    response_class=JSONResponse,
    response_model=CountDB,
    status_code=200,
    responses={
        200: {"description": "Total dogs"},
    },
)
async def count(search: SearchDog = Depends(SearchDog)):
    """
    Count dogs that satisfy the parameters entered.
    **Args**:
    - **Headers**:
        - accept: application/json
    - **Query Params**:
        - **name** (str, optional): name of the dog.
        - **description** (str, optional): description of the dog.
    **Returns**:
    - **200** (JSON):
        - **count** (int): Total dogs.
    - **400** (JSON): Bad Request
    - **401** (JSON): The user doesn't have enough privileges
    - **422** (JSON): Unprocessable Entity
    - **500** (JSON): Internal Server Error (Please, contact administrators)
    """
    dog = await dog_service.count(payload=search.dict(exclude_none=True))
    return {"count": dog}


@router.post(
    "",
    response_class=JSONResponse,
    response_model=Dog,
    status_code=201,
    responses={
        201: {"description": "Dog created"},
    },
)
async def create(new_dog: CreateDog):
    """
    Create a new Dog for a haul.
    **Args**:
    - **Headers**:
        - accept: application/json
        - Content-Type: application/json
    - **Request Body**:
        - **name** (str): name of the Dog.
        - **description** (str, optional): description of the Dog.
    **Returns**:
    - **201** (JSON):
        - **name** (str, optional): name of the Dog.
        - **description** (str, optional): description of the Dog.
        - **id** (int): Database id corresponding to the created Dog.
        - **created_at** (datetime): Date of creation of the Dog in the database (UTC time)
    - **400** (JSON): Bad Request
    - **401** (JSON): The user doesn't have enough privileges
    - **422** (JSON): Unprocessable Entity
    - **500** (JSON): Internal Server Error (Please, contact administrators)
    """
    dog = await dog_service.create(obj_in=new_dog)
    return dog


@router.get(
    "/{id}",
    response_class=JSONResponse,
    response_model=Dog,
    status_code=200,
    responses={
        200: {"description": "Dog found"},
        404: {"description": "Dog not found"},
    },
)
async def by_id(id: int = Path(...)):
    """
    Get a Dog by id.
    **Args**:
    - **Headers**:
        - accept: application/json
    - **Path Params**:
        - **id** (int): Database id corresponding to the Dog.
    **Returns**:
    - **200** (JSON):
        - **name** (str, optional): name of the Dog.
        - **description** (str, optional): description of the Dog.
        - **id** (int): Database id corresponding to the Dog.
        - **created_at** (datetime): Date of creation of the Dog in the database (UTC time)
        - **last_modified** (datetime): Date of the last modification of the Dog in the database (UTC time)
    - **400** (JSON): Bad Request
    - **401** (JSON): The user doesn't have enough privileges
    - **404** (JSON): Object does not exist
    - **422** (JSON): Unprocessable Entity
    - **500** (JSON): Internal Server Error (Please, contact administrators)
    """
    dog = await dog_service.get_byid(id=id)
    if dog is None:
        raise HTTPException(status_code=404, detail="dog not found")
    return dog


@router.patch(
    "/{id}",
    response_class=Response,
    response_model=None,
    status_code=204,
    responses={
        204: {"description": "Dog update"},
        404: {"description": "Dog not found"},
    },
)
async def update(update_dog: UpdateDog, id: int = Path(...)):
    r"""
    Update an existing Dog by id.
    **Args**:
    - **Headers**:
        - accept: \*/*
        - Content-Type: application/json
    - **Path Params**:
        - **id** (int): Database id corresponding to the Dog.
    - **Request Body**:
        - **nmfc** (str, optional): The National Motor Freight Classification sent by the customer.
        - **nmfc_calculated** (str, optional): The National Motor Freight Classification Calculated.
        - **dimensions** (str, optional): Dog dimensions, must be in the format: float(length) x float(width) x float(height) inch, e.g. 48 x 40 x 35 inch.
        - **hu_count** (str, optional): Dog handling units count, must be in the format: int(hu_inch) Pallets, e.g. 2 Pallets.
        - **weight** (str, optional): Dog weight, must be in the format: float(weight) lb, e.g. 200.0 lb.
        - **description** (str, optional): Dog description.
        - **contribution** (str, optional): contribution of the dog to the total haul.
    **Returns**:
    - **204** (No Body)
    - **400** (JSON): Bad Request
    - **401** (JSON): The user doesn't have enough privileges
    - **404** (JSON): Object does not exist
    - **422** (JSON): Unprocessable Entity
    - **500** (JSON): Internal Server Error (Please, contact administrators)
    """
    dog = await dog_service.update(id=id, obj_in=update_dog)
    if dog is False:
        raise HTTPException(status_code=404, detail="Dog not found")


@router.delete(
    "/{id}",
    response_class=Response,
    response_model=None,
    status_code=204,
    responses={
        204: {"description": "Dog delete"},
    },
)
async def delete(id: int = Path(...)):
    r"""
    Delete a dog by id.
    **Args**:
    - **Headers**:
        - accept: \*/*
    - **Path Params**:
        - **id** (int): Database id corresponding to the dog.
    **Returns**:
    - **204** (No Body)
    - **400** (JSON): Bad Request
    - **401** (JSON): The user doesn't have enough privileges
    - **404** (JSON): Dog not found
    - **422** (JSON): Unprocessable Entity
    - **500** (JSON): Internal Server Error (Please, contact administrators)
    """
    dog = await dog_service.delete(id=id)
    if dog == 0:
        raise HTTPException(status_code=404, detail="Dog not found")
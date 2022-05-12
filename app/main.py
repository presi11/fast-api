from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.config import settings
from app.debugger import initialize_fastapi_server_debugger_if_needed
from app.infra.postgres.config import (
    generate_records_defaults,
    generate_schema,
    init_db,
)


def create_application():
    initialize_fastapi_server_debugger_if_needed()

    app = FastAPI(
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
    )
    app.include_router(api_router, prefix="/api")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


app = create_application()


@app.on_event("startup")
async def startup_event():
    init_db(app)
    await generate_schema()
    if settings.DEFAULT_DATA:
        await generate_records_defaults()
# from datetime import datetime
# from turtle import pos
# from typing import Text
# import uuid
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import Text, Optional
# from uuid import uuid4 as uuid

# app = FastAPI() 

# # Post Model
# class Post(BaseModel):
#     id: str
#     title: str
#     author: str
#     content: Text
#     create_at: datetime = datetime.now()
#     published_at: Optional[datetime]
#     published: bool = False

# posts = []

# @app.get('')
# def read_root():
#         return{"welcome"}

# @app.get('/posts')
# def get_posts():
#         return posts

# @app.post('/posts')
# def save_post(post: Post):
#     post.id = str(uuid())
#     posts.append(post.dict())
#     return posts[-1]

# @app.get('/posts/{post_id}')
# def get_post(post_id: str):
#         for post in posts:
#                 if posts["id"] == post_id:
#                         return post
#         raise HTTPException(status_code=404, detail="post not found") 

# @app.delete("/posts/{post_id}")
# def delete_post(post_id: str):
#         for index,post in enumerate(posts):
#                 if post["id"]== post_id:
#                         posts.pop(index)
#                         return {"message": "Post delete succeess"}
#         raise HTTPException(status_code=404, detail="post not found") 


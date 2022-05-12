from cgi import print_arguments
from json import load as json_load
from logging import getLogger
from os import listdir

from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from app.config import settings

log = getLogger(__name__)


TORTOISE_ORM = {
    "connections": {"default": settings.POSTGRES_DATABASE_URL},
    "apps": {
        "models": {
            "models": ["app.infra.postgres.models"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=settings.POSTGRES_DATABASE_URL,
        modules={"models": ["app.infra.postgres.models"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )


async def generate_schema() -> None:
    log.info("Initializing Tortoise...")
    print(settings.POSTGRES_DATABASE_URL)
    await Tortoise.init(
        db_url=settings.POSTGRES_DATABASE_URL,
        modules={"models": ["app.infra.postgres.models"]},
    )
    log.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()


async def generate_records_defaults():
    files = [file for file in listdir("./storage/default") if file.endswith(".json")]
    files = sorted(files, key=lambda file: file.split("_")[0])

    IMPORTS = "from app.infra.postgres.models.{} import {}"
    for file in files:
        if not settings.DEFAULT_DEV_DATA and "dev" in file:
            continue
        with open(f"./storage/default/{file}") as file:
            default_data = json_load(file)

        python_file = default_data["file"]
        model = default_data["model"]
        create_default = f"await {model}.get_or_create(**data)"
        default_data = default_data["data"]
        function = (
            "async def __ex(data):"
            f"\n\t{IMPORTS.format(python_file, model)}\n\t{create_default}"
        )
        for data in default_data:
            try:
                exec(function)
                await locals()["__ex"](data)
            except Exception as e:
                print(e)
                continue

    await Tortoise.close_connections()
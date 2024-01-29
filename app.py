from fastapi import FastAPI
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise
from typing import List, Optional

import logging

from config import PSQLConfig
from service.models.pydantic_models import (
    CategoryPydantic,
    ManufacturerPydantic,
    ModelPydantic,
    PartPydantic,
)
from service.views.category_view import CategoryView
from service.views.manufacturer_view import ManufacturerView
from service.views.model_view import ModelView
from service.views.part_view import PartView


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

description = """
URParts API allows you to get manufacturers, categories, models, parts. 🚀

## Manufacturers

You can **get manufacturers** list.

## Categories

You can **get categories** list.

## Models

You can:
* **get model by id** 
* **get all models** (optional of specific _manufacturer_)

## Parts

You can:
* **get part by id** 
* **get parts for a model** (optional for specific _category_ of parts)
* **get all models for part** which are compatible with this part
"""

app = FastAPI(
    title="URParts",
    description=description,
    summary="Web-service to get parts and related information",
    version="0.0.1",
    contact={
        "name": "Pavel Mikheev",
        "url": "https://github.com/mikheev-dev",
        "email": "mikheevpav@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

register_tortoise(
    app,
    db_url=PSQLConfig.connection_string(),
    modules={"models": ["service.models.db_models"]},
    generate_schemas=False,
    add_exception_handlers=True,
)


class Status(BaseModel):
    message: str


@app.get("/manufacturers", response_model=List[ManufacturerPydantic])
async def get_manufacturers():
    return await ManufacturerView.get_all_manufacturers()


@app.get("/categories", response_model=List[CategoryPydantic])
async def get_categories():
    return await CategoryView.get_all_categories()


@app.get("/model/{model_id}", response_model=ModelPydantic)
async def get_model_by_id(model_id: int):
    return await ModelView.get_model_by_id(model_id=model_id)


@app.get("/models", response_model=List[ModelPydantic])
async def get_models(manufacturer_name: Optional[str] = None):
    return await ModelView.get_models(manufacturer_name=manufacturer_name)


@app.get("/parts/{model_id}", response_model=List[PartPydantic])
async def get_parts_for_model(model_id: int, category_name: Optional[str] = None):
    return await PartView.get_parts_for_model(model_id=model_id, category_name=category_name)


@app.get("/part/{part_id}", response_model=PartPydantic)
async def get_part_by_id(part_id: int):
    return await PartView.get_part_by_id(part_id=part_id)


@app.get("/models_for_part/{part_id}", response_model=List[ModelPydantic])
async def get_part_compatible_models(part_id: int):
    return await PartView.get_part_compatible_models(part_id=part_id)


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

app = FastAPI(title="URParts")

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


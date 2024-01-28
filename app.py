from fastapi import FastAPI
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise
from tortoise.expressions import Q
from typing import List, Optional

from config import PSQLConfig
from db_models import (
    Category,
    Manufacturer,
    Model,
    Part,
)
from pydantic_models import (
    CategoryPydantic,
    ManufacturerPydantic,
    ModelPydantic,
    PartPydantic,
)


app = FastAPI(title="URParts")

register_tortoise(
    app,
    db_url=PSQLConfig.connection_string(),
    modules={"models": ["db_models"]},
    generate_schemas=False,
    add_exception_handlers=True,
)


class Status(BaseModel):
    message: str


@app.get("/manufacturers", response_model=List[ManufacturerPydantic])
async def get_manufacturers():
    return await ManufacturerPydantic.from_queryset(Manufacturer.all())


@app.get("/categories", response_model=List[CategoryPydantic])
async def get_categories():
    return await CategoryPydantic.from_queryset(Category.all())


@app.get("/model/{model_id}", response_model=ModelPydantic)
async def get_model(model_id: int):
    return await ModelPydantic.from_queryset_single(Model.get(id=model_id))


@app.get("/models", response_model=List[ModelPydantic])
async def get_models(manufacturer_name: Optional[str] = None):
    if not manufacturer_name:
        models = Model.all()
    else:
        models = Model.filter(manufacturer__name=manufacturer_name)

    return await ModelPydantic.from_queryset(models)


@app.get("/parts/{model_id}", response_model=List[PartPydantic])
async def get_parts_for_model(model_id: int, category_name: Optional[str] = None):
    if not category_name:
        parts = Part.filter(models__id=model_id)
    else:
        parts = Part.filter(Q(models__id=model_id) & Q(categories__name=category_name))
    return await PartPydantic.from_queryset(parts)

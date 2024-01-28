from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from db_models import (
    Category,
    Manufacturer,
    Model,
    Part,
)

Tortoise.init_models(['db_models'], "models")

CategoryPydantic = pydantic_model_creator(Category)
ManufacturerPydantic = pydantic_model_creator(Manufacturer)
ModelPydantic = pydantic_model_creator(Model)
PartPydantic = pydantic_model_creator(Part)

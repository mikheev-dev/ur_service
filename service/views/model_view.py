from fastapi import HTTPException
from tortoise.exceptions import OperationalError, DoesNotExist
from typing import List, Optional

import logging

from service.models.pydantic_models import ModelPydantic
from service.models.db_models import Model


logger = logging.getLogger(__name__)


class ModelView:
    @staticmethod
    async def get_model_by_id(model_id: int) -> ModelPydantic:
        try:
            return await ModelPydantic.from_queryset_single(Model.get(id=model_id))
        except DoesNotExist as e:
            raise e
        except OperationalError as e:
            logger.error(f"Exception {e} occurred")
            raise HTTPException(status_code=404, detail=f"Model {model_id} is not ready.")

    @staticmethod
    async def get_models(manufacturer_name: Optional[str] = None) -> List[ModelPydantic]:
        try:
            if not manufacturer_name:
                models = Model.all()
            else:
                models = Model.filter(manufacturer__name=manufacturer_name)

            return await ModelPydantic.from_queryset(models)
        except OperationalError as e:
            logger.error(f"Exception {e} occurred")
            raise HTTPException(status_code=404, detail=f"Models are not ready.")

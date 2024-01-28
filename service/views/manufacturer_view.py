from fastapi import HTTPException
from tortoise.exceptions import OperationalError
from typing import List

import logging

from service.models.pydantic_models import ManufacturerPydantic
from service.models.db_models import Manufacturer


logger = logging.getLogger(__name__)


class ManufacturerView:
    @staticmethod
    async def get_all_manufacturers() -> List[ManufacturerPydantic]:
        try:
            return await ManufacturerPydantic.from_queryset(Manufacturer.all())
        except OperationalError as e:
            logger.error(f"Exception {e} occurred.")
            raise HTTPException(status_code=404, detail="Manufacturers are not ready.")

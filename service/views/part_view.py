from fastapi import HTTPException
from tortoise.exceptions import OperationalError
from tortoise.expressions import Q
from typing import List, Optional, Tuple

import asyncio
import logging

from service.models.pydantic_models import PartPydantic, ModelPydantic
from service.models.db_models import Part, Model


logger = logging.getLogger(__name__)


class PartView:
    @staticmethod
    async def get_part_by_id(part_id: int) -> PartPydantic:
        try:
            return await PartPydantic.from_queryset_single(Part.get(id=part_id))
        except OperationalError as e:
            logger.error(f"Exception {e} occurred")
            raise HTTPException(status_code=404, detail=f"Part {part_id} is not ready.")

    @staticmethod
    async def get_parts_for_model(
            model_id: int,
            category_name: Optional[str] = None
    ) -> List[PartPydantic]:
        try:
            if not category_name:
                parts = Part.filter(models__id=model_id)
            else:
                parts = Part.filter(Q(models__id=model_id) & Q(categories__name=category_name))
            return await PartPydantic.from_queryset(parts)
        except OperationalError as e:
            logger.error(f"Exception {e} occurred")
            raise HTTPException(status_code=404, detail=f"Parts are not ready.")

    @staticmethod
    async def get_part_compatible_models(part_id: int) -> List[ModelPydantic]:
        try:
            part = await Part.get(id=part_id).prefetch_related("models", "models__manufacturer")
            return list(await asyncio.gather(*[
                ModelPydantic.from_tortoise_orm(m)
                for m in part.models
            ]))
        except OperationalError as e:
            logger.error(f"Exception {e} occurred")
            raise HTTPException(status_code=404, detail=f"Part {part_id} are not ready.")

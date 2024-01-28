from fastapi import HTTPException
from tortoise.exceptions import OperationalError
from typing import List

import logging

from service.models.pydantic_models import CategoryPydantic
from service.models.db_models import Category


logger = logging.getLogger(__name__)


class CategoryView:
    @staticmethod
    async def get_all_categories() -> List[CategoryPydantic]:
        try:
            return await CategoryPydantic.from_queryset(Category.all())
        except OperationalError as e:
            logger.error(f"Exception {e} occurred.")
            raise HTTPException(status_code=404, detail="Categories are not ready.")

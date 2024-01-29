from fastapi.exceptions import HTTPException

import pytest

from tortoise.exceptions import DoesNotExist
from service.views.part_view import PartView
from tests.utils import init_db, close_db


class TestPartView:
    @pytest.mark.asyncio
    async def test_get_part_by_id_no_table(self):
        await init_db()

        part_id = 812
        with pytest.raises(HTTPException) as exc_info:
            await PartView.get_part_by_id(part_id=part_id)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == f"Part {part_id} is not ready."

        await close_db()

    @pytest.mark.asyncio
    async def test_get_part_by_id_no_object(self):
        await init_db(create_schemas=True)

        part_id = 812
        with pytest.raises(DoesNotExist):
            await PartView.get_part_by_id(part_id=part_id)

        await close_db()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("category", ["a", None])
    async def test_get_parts_for_model_no_table(self, category):
        await init_db()

        model_id = 812
        with pytest.raises(HTTPException) as exc_info:
            await PartView.get_parts_for_model(model_id=model_id, category_name=category)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == f"Parts are not ready."

        await close_db()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("category", ["a", None])
    async def test_get_parts_for_model_no_model(self, category):
        await init_db(create_schemas=True)

        model_id = 812

        with pytest.raises(DoesNotExist):
            await PartView.get_parts_for_model(model_id=model_id, category_name=category)

        await close_db()

    @pytest.mark.asyncio
    async def test_get_part_compatible_models_no_table(self):
        await init_db()

        part_id = 812
        with pytest.raises(HTTPException) as exc_info:
            await PartView.get_part_compatible_models(part_id=part_id)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == f"Part {part_id} is not ready."

        await close_db()

    @pytest.mark.asyncio
    async def test_get_part_compatible_models_no_part(self):
        await init_db(create_schemas=True)

        part_id = 812
        with pytest.raises(DoesNotExist):
            await PartView.get_part_compatible_models(part_id=part_id)

        await close_db()

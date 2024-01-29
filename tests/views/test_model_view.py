import pytest

from fastapi.exceptions import HTTPException
from tortoise.exceptions import DoesNotExist
from service.views.model_view import ModelView
from tests.utils import init_db, close_db


class TestModelView:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("manufacturer_name", ["A", None])
    async def test_get_models_no_table(self, manufacturer_name):
        await init_db()

        with pytest.raises(HTTPException) as exc_info:
            await ModelView.get_models(manufacturer_name)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Models are not ready."

        await close_db()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("manufacturer_name", ["A", "1243"])
    async def test_get_models_for_not_existed_manufacturer(self, manufacturer_name):
        await init_db(create_schemas=True)

        models = await ModelView.get_models(manufacturer_name)
        assert len(models) == 0

        await close_db()

    @pytest.mark.asyncio
    async def test_get_model_by_id_no_table(self):
        await init_db()

        model_id = 812
        with pytest.raises(HTTPException) as exc_info:
            await ModelView.get_model_by_id(model_id=model_id)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == f"Model {model_id} is not ready."

        await close_db()

    @pytest.mark.asyncio
    async def test_get_model_by_id_no_object(self):
        await init_db(create_schemas=True)

        model_id = 812
        with pytest.raises(DoesNotExist):
            await ModelView.get_model_by_id(model_id=model_id)

        await close_db()

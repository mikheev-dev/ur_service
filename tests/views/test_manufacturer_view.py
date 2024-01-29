import pytest

from fastapi.exceptions import HTTPException
from service.views.manufacturer_view import ManufacturerView
from tests.utils import init_db, close_db


class TestManufacturerView:
    @pytest.mark.asyncio
    async def test_get_all_manufacturers_no_table(self):
        await init_db()

        with pytest.raises(HTTPException) as exc_info:
            await ManufacturerView.get_all_manufacturers()

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Manufacturers are not ready."

        await close_db()

    @pytest.mark.asyncio
    async def test_get_all_manufacturers_empty_table(self):
        await init_db(create_schemas=True)

        manufacturers = await ManufacturerView.get_all_manufacturers()
        assert len(manufacturers) == 0

        await close_db()


import pytest

from fastapi.exceptions import HTTPException
from service.views.category_view import CategoryView
from tests.utils import init_db, close_db


class TestCategoriesView:
    @pytest.mark.asyncio
    async def test_get_all_categories_no_table(self):
        await init_db()

        with pytest.raises(HTTPException) as exc_info:
            await CategoryView.get_all_categories()

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Categories are not ready."

        await close_db()

    @pytest.mark.asyncio
    async def test_get_all_categories_empty_table(self):
        await init_db(create_schemas=True)

        categories = await CategoryView.get_all_categories()
        assert len(categories) == 0

        await close_db()


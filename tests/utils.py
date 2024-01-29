from tortoise import Tortoise


async def init_db(create_schemas=False):
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["service.models.db_models"]},
    )
    if create_schemas:
        await Tortoise.generate_schemas()


async def close_db():
    await Tortoise._drop_databases()
    await Tortoise.close_connections()

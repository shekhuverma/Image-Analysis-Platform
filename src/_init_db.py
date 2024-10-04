import asyncio

from src.db import database, services
from src.schemas import user
from src.settings import config

# To add the superuser to newly created database
asyncio.run(
    services.create_user(
        user.CreateUser(
            username=config.BASEUSER,
            email=config.BASEUSER_EMAIL,
            password=config.BASEUSER_PASSWORD,
        ),
        database.SessionLocal(),
    )
)

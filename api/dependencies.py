"""Dependency injection file"""

import os
from typing import AsyncGenerator

import motor.motor_asyncio
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorDatabase

load_dotenv()


client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["DATABASE_URL"])
db = client.get_database("test")


async def get_db() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    """Motor DB dependency injection

    Returns
    -------
    AsyncGenerator[AsyncIOMotorDatabase, None]

    Yields
    ------
    Iterator[AsyncGenerator[AsyncIOMotorDatabase, None]]

    Raises
    ------
    e
        Generic exception
    """
    try:
        yield db
    except Exception as e:
        raise e

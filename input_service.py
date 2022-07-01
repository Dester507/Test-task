import os
import asyncio

import aiohttp
from motor import motor_asyncio
from pymongo.errors import OperationFailure


async def override_gather(n: int, *tasks):
    # Init Semaphore
    semaphore = asyncio.Semaphore(n)

    async def make_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(*(make_task(task) for task in tasks))


async def get_func(url: str, session: aiohttp.ClientSession, results: list):
    async with session.get(url) as response:
        body = await response.json()
        results.append(body)


async def repeat(interval, func, *args, **kwargs):
    while True:
        await asyncio.gather(
            func(*args, **kwargs),
            asyncio.sleep(interval)
        )


async def repeated_task(
        urls: list,
        threads: int,
        session: aiohttp.ClientSession,
        client: motor_asyncio.AsyncIOMotorClient
):
    results = []
    # Parallel requests
    await override_gather(threads, *[get_func(url, session, results) for url in urls])
    # Save in to db
    await client.test_database.test_collection.insert_many(results)
    print("saved")


async def main():
    # Connect to MongoDB
    conn_str = os.getenv("DATABASE_URL")
    mongo_client = motor_asyncio.AsyncIOMotorClient(conn_str)
    try:
        # Check if connected
        await mongo_client.server_info()
        # Aiohttp
        conn = aiohttp.TCPConnector(limit=None)
        session = aiohttp.ClientSession(connector=conn)
        urls = [f"http://135.181.197.58:8000/api/v1/weather/source_{x}" for x in range(1, 6)]
        threads_limit = 5
        # Send request every 10 seconds
        await repeat(10, repeated_task, urls, threads_limit, session, mongo_client)
    except OperationFailure:
        print("Unable to connect to the server.")


asyncio.run(main())

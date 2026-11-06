import asyncio
import time
from collections.abc import Awaitable
from typing import TypeVar

import httpx

T = TypeVar("T")

URLS = ["https://httpbin.org/delay/2"] * 10 + [
    "https://httpbin.org/status/404",
    "htt://salam.super//",
    "https://httpbin.org/delay/10",
]


async def check(
    client: httpx.AsyncClient, sem: asyncio.Semaphore, url: str
) -> tuple[str, int | str]:
    try:
        async with sem:
            response = await client.get(url)
            return (url, response.status_code)
    except httpx.HTTPError as e:
        return (url, type(e).__name__)


async def run_gather(
    client: httpx.AsyncClient, sem: asyncio.Semaphore, urls: list[str]
) -> list[tuple[str, int | str]]:
    return list(await asyncio.gather(*(check(client, sem, u) for u in urls)))


async def run_sequential(
    client: httpx.AsyncClient, sem: asyncio.Semaphore, urls: list[str]
) -> list[tuple[str, int | str]]:
    return [await check(client, sem, u) for u in urls]


async def timed[T](label: str, coro: Awaitable[T]) -> T:
    start = time.perf_counter()
    result = await coro
    print(f"{label}: {time.perf_counter() - start:.1f}s")
    return result


async def main() -> None:
    sem = asyncio.Semaphore(5)
    async with httpx.AsyncClient(timeout=5.0, follow_redirects=True) as client:
        await timed("gather(5)", run_gather(client, sem, URLS))
        await timed("ardicil", run_sequential(client, sem, URLS))


asyncio.run(main())

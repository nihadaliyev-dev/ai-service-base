import asyncio
import time


async def fake_call(name: str, seconds: float) -> str:
    await asyncio.sleep(seconds)
    return f"{name} done"


async def main() -> None:
    t = time.perf_counter()
    for i in range(3):
        await fake_call(f"call{i}", 1)
    print(f"ardicil: {time.perf_counter() - t:.1f}s")

    t = time.perf_counter()
    await asyncio.gather(*(fake_call(f"call{i}", 1) for i in range(3)))
    print(f"paralel: {time.perf_counter() - t:.1f}s")


asyncio.run(main())

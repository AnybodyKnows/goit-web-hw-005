import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import random


async def ping(signal):
    print(f"Received signal {signal}")


async def ping_worker():
    while True:
        await asyncio.sleep(1)
        await ping(random.randint(1, 1000))


def cpu_bound_operations(counter: int):
    init = counter
    while counter > 0:
        counter -= 1
    print(f"Completed{init}")
    return init


async def main():
    loop = asyncio.get_running_loop()
    task = loop.create_task(ping_worker())

    with ProcessPoolExecutor(2) as pool:
        f = [loop.run_in_executor(pool, cpu_bound_operations, counter) for counter in [100000000, 120000000, 150000000]]
        result = await asyncio.gather(*f)
        task.cancel()
        return result


if __name__ == '__main__':
    result = asyncio.run(main())
    print(result)

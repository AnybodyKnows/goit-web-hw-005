import asyncio
import random


async def ping(signal):
    print(f"Received signal {signal}")


async def main():
    while True:
        await asyncio.sleep(1)
        await ping(random.randint(1, 1000))


if __name__ == "__main__":
    asyncio.run(main())

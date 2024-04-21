import asyncio
from random import randint


async def producer(q: asyncio.Queue):
    num = randint(1, 1000)
    await asyncio.sleep(0.1)
    await q.put(num)


async def consumer(q: asyncio.Queue):
    while True:
        num = await q.get()
        print(f"Received {num ** 2}")
        q.task_done()


async def main():
    queue = asyncio.Queue()
    consumer_task = [asyncio.create_task(consumer(queue)) for _ in range(3)]
    producer_task = [asyncio.create_task(producer(queue)) for _ in range(100)]
    await asyncio.gather(*producer_task)
    await queue.join()
    [task.cancel() for task in consumer_task]


if __name__ == '__main__':
    asyncio.run(main())

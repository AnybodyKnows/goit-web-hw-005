import asyncio
from faker import Faker
from time import sleep, time
import Timing

fake = Faker("uk-UA")


async def async_get_user_from_db(uuid: int, future: asyncio.Future):
    await asyncio.sleep(0.5)
    future.set_result({"id": uuid, "name": fake.user_name(), "email": fake.email()})


def make_request(uuid: int) -> asyncio.Future:
    future = asyncio.Future()
    asyncio.create_task(async_get_user_from_db(uuid, future))
    return future


@Timing.async_timed("Check Time")
async def main():
    users = []
    for i in range(1, 6):
        users.append(make_request(i))
    print(users)
    result = await asyncio.gather(*users)
    print(users)
    return result


if __name__ == "__main__":
    users = asyncio.run(main())
    print(users)

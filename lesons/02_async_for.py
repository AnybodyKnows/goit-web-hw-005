import asyncio
from faker import Faker
from Timing import async_timed
from typing import Iterable, Awaitable, Coroutine, Any

fake = Faker("uk-UA")


async def get_user_from_db(uuid: int):
    await asyncio.sleep(0.5)
    return {"id": uuid, "name": fake.user_name(), "email": fake.email()}


async def get_users(uuids: list[int]) -> list[Coroutine[int, Any, dict]]:
    return [get_user_from_db(pk) for pk in uuids]


@async_timed("______________________main__________________________________________")
async def main(users: Coroutine[int, Any, list[Coroutine[int, Any, dict]]]):
    users = [user for user in await users]
    result = await asyncio.gather(*users)
    return result


if __name__ == "__main__":
    r = asyncio.run(main(get_users([1, 2, 3])))
    print(r)

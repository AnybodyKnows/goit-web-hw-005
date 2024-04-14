import asyncio


async def foo():
    await asyncio.sleep(0)
    return "Hello world"


async def main():
    result = foo()
    return await result


if __name__ == "__main__":
    r = asyncio.run(main())
    print(r)




import requests
from concurrent.futures import ThreadPoolExecutor
import asyncio
from Timing import async_timed, sync_timed
from requests.exceptions import InvalidSchema, MissingSchema, SSLError

urls = [
    "http://www.twitter.com",
    "http://www.instagram.com",
    "http://www.linkedin.com",
    "http://www.pinterest.com",
    "http://www.tumblr.com",
    "http://www.youtube.com",
    "asdfsdf",
    "http://www.dropbox.com"]


def get_preview(url: str) -> tuple[str, str]:
    res = requests.get(url)
    return f"/n {url}", res.text[:25]


@sync_timed()
def main_sync():
    results = []
    for url in urls:
        try:
            results.append(get_preview(url))
        except (InvalidSchema, MissingSchema, SSLError) as e:
            print(e)
    return results


@async_timed()
async def main():
    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor(10) as pool:
        futures = [loop.run_in_executor(pool, get_preview, url) for url in urls]
        results = await asyncio.gather(*futures, return_exceptions=True)
    return results


if __name__ == "__main__":
    print(main_sync())

    r = list(asyncio.run(main()))
    for el in r:
        if isinstance(el, Exception):
            r.remove(el)
    print(r)

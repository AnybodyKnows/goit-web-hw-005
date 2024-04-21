import aiohttp
import asyncio
import json
from datetime import datetime, timedelta
import sys


class HttpError(Exception):
    pass


async def request(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    result = json.dumps(result, indent=4)
                    return result
                else:
                    raise HttpError(f"Error status: {resp.status} for {url}")
        except (aiohttp.ClientConnectorError, aiohttp.InvalidURL) as err:
            raise HttpError(f'Connection error: {url}', str(err))


async def main(index_date: 0, ccy: ""):
    ccy_list = ["USD", "EUR", ccy]
    all_date_output = []
    index_date += 1
    if index_date > 10:
        index_date = 10
    for i in range(index_date):
        dat = datetime.now() - timedelta(days=i)
        dat = datetime.strftime(dat, format="%d.%m.%Y")
        try:
            response = await request(f"https://api.privatbank.ua/p24api/exchange_rates?json&date={dat}")
            response = json.loads(response)
            fx_output = {}
            fx = response["exchangeRate"]
            for el in fx:
                if el["currency"] in ccy_list:
                    fx_output[el["currency"]] = {"sale": el["saleRate"], "purchase": el["purchaseRate"]}
            single_date_output = {dat: fx_output}
            all_date_output.append(single_date_output)
        except HttpError as err:
            print(err)
    return json.dumps(all_date_output, indent=2)

if __name__ == '__main__':
    r = asyncio.run(main(int(sys.argv[1]), sys.argv[2]))
    print(sys.argv)
    print(r)

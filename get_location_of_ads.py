import sys
import asyncio
import sqlite3
import time

import aiohttp
from aiohttp import ClientOSError
from ad_specific_parser import get_coordinates

ads_count = 0


async def http_client(session, url):
    global ads_count

    async with session.get(url) as response:
        text = await response.text()
        if response.status == 403:
            print("ip ban")
            print(ads_count)
            sys.exit()

        ads_count += 1
        if ads_count % 100 == 0:
            print(ads_count)
        return text, url


async def get_location_from_link(connection):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive',
    }

    my_timeout = aiohttp.ClientTimeout(
        total=None,  # default value is 5 minutes, set to `None` for unlimited timeout
        sock_connect=None,  # How long to wait before an open socket allowed to connect
        sock_read=None,  # How long to wait with no data being read before timing out
    )

    cursor = connection.cursor()

    QUERY = "SELECT link FROM ads WHERE latitude is NULL AND longitude is NULL AND error_link is NULL"

    async with aiohttp.ClientSession(headers=headers, timeout=my_timeout) as session:

        cursor.execute(QUERY)
        ads = cursor.fetchall()

        if len(ads) == 0:
            print("all ads have location or error link")
            sys.exit()

        test = 100
        while ads:

            location_collection_tasks = (http_client(session, url_tuple[0]) for url_tuple in ads[:test])
            location_data = await asyncio.gather(*location_collection_tasks)
            # await asyncio.sleep(1)
            del ads[:test]

            for data in location_data:
                text, url = data
                latitude, longitude, error_link = get_coordinates(text, url=url, covert_to_soup=True)
                QUERY = "UPDATE ads set latitude=?, longitude=?, error_link=? where link=?"
                cursor.execute(QUERY, (latitude, longitude, error_link, url))
                connection.commit()


if __name__ == "__main__":

    t1 = time.perf_counter()
    connection = sqlite3.connect('fundanew.db')
    while True:
        try:
            asyncio.run(get_location_from_link(connection))
        except ClientOSError as error:
            print(error)
            # time.sleep(10)
    print(time.perf_counter() - t1)

import asyncio
import sqlite3
import time

import uvloop

from get_total_pages import get_total_pages
from scraper import ads_all_details, ads_listed_details
from aiohttp_client import aiohttp_client

from sqlite_setup_create_table import create_new_table

uvloop.install()


def get_all_page_links(first_page=1):
    url = "https://www.funda.nl/koop/heel-nederland/"
    # total_page_numbers = get_total_pages(url)
    total_page_numbers = 1
    for page in range(first_page, total_page_numbers + 1):
        yield f"{url}p{page}/"


async def main():

    new_connection = sqlite3.connect('fundanew.db')
    create_new_table()

    async with aiohttp_client() as session:
        page_specific_tasks_collection = (ads_all_details(session, url, new_connection) for url in get_all_page_links())
        await asyncio.gather(*page_specific_tasks_collection)

    new_connection.commit()
    new_connection.close()


if __name__ == "__main__":
    t1 = time.perf_counter()
    print("started")
    asyncio.run(main())
    print(time.perf_counter() - t1)

import asyncio
import sqlite3
import time


import uvloop

from get_total_pages import get_total_pages
from scraper import ads_all_details, ads_listed_details

from aiohttp_client import aiohttp_client

from sqlite_setup_create_table import create_new_table
from compress_file import compress_file

uvloop.install()


# START_URL = "https://www.funda.nl/koop/heel-nederland/"
START_URL = "https://www.funda.nl/koop/heel-nederland/sorteer-datum-af/"


def get_all_page_links(START_URL, first_page=1):
    # final_page = get_total_pages(START_URL)
    page = input("enter page numbers example 10-100: ")
    page = page.split("-")

    final_page = int(page[-1])
    if len(page) == 2:
        first_page = int(page[0])

    for page in range(first_page, final_page + 1):
        yield f"{START_URL}p{page}/"


async def main():
    new_connection = sqlite3.connect('fundanew.db')
    create_new_table()

    async with aiohttp_client() as session:
        page_specific_tasks_collection = (
            ads_all_details(session, url, new_connection, START_URL) for url in get_all_page_links(START_URL)
        )

        try:
            await asyncio.gather(*page_specific_tasks_collection)
        except asyncio.CancelledError:
            # debug helped to show there was no error message and this is the exception raised
            # # except BaseException as e: e can let us know which exception is raised
            print("KeyboardInterrupt error should be catched")
            # might causedb corruption
            # new_connection.commit()

        else:
            new_connection.commit()

        finally:
            new_connection.close()
            new_connection.close()
            compress_file("fundanew.db", "archive.7z")


async def batch_main():
    create_new_table()

    async with aiohttp_client() as session:
        page_links = list(get_all_page_links(START_URL))
        task_number_per_loop = 2000
        page_links_part_lists = [
            page_links[i : i + task_number_per_loop] for i in range(0, len(page_links) + 1, task_number_per_loop)
        ]

        file_count = 0
        for link_list in page_links_part_lists:
            new_connection = sqlite3.connect('fundanew.db')
            page_specific_tasks_collection = (
                ads_all_details(session, url, new_connection, START_URL) for url in link_list
            )

            try:
                await asyncio.gather(*page_specific_tasks_collection)
            except asyncio.CancelledError:
                print("KeyboardInterrupt error should be catched")

            else:
                new_connection.commit()
                file_count += 1

            finally:
                new_connection.close()
                compress_file("fundanew.db", f"archive{file_count}.7z")


if __name__ == "__main__":
    t1 = time.perf_counter()
    print("started")
    try:
        print(time.ctime())
        asyncio.run(main())
    except KeyboardInterrupt:
        print("collecting ads are stopped as instructed KeyboardInterrupt")
    print(time.perf_counter() - t1)

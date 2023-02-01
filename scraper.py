import asyncio
import time
import os
import gc

from datetime import datetime, timezone

from insert_data import insert_ads

from ads_listed_parser import ads_listed_parser

from ad_specific_parser import ad_specific_parser_and_insert_db

import psutil

pages = 0
html_check = 0


def memory_usage():
    print(psutil.Process(os.getpid()).memory_info().rss / 1024**2)
    print(time.ctime(), html_check, len(asyncio.all_tasks()))


def debug_response(response_text):
    with open('temp.html', 'w') as f:
        f.write(response_text)


async def ads_all_details(session, url, connection, start_url):
    """
    Function ads_all_details scraps list of ads in a given url and specific details of all ads in this page recursively
    start_url parameter helps to classify url to page url or ad specific url
    we keep track of total number of each type of url that is properly scraped

    # 20 pages
    # with db insert
    # 32.751898002001326
    # just parsing
    # 21.446617995999986
    """

    global pages
    global html_check

    async with session.get(url) as response:
        text = await response.text()

    if not url.startswith(start_url):
        # here url is ad specific details page url
        html_check += 1
        cursor = connection.cursor()
        # cursor.execute("SELECT id from ads where link = ?", (url,))
        # ad_id = cursor.fetchone()[0]
        ad_id = cursor.execute("SELECT id from ads where link = ?", (url,)).fetchone()[0]

        ad_specific_parser_and_insert_db(text, ad_id, url, connection)

        if html_check % 100 == 0:
            connection.commit()
            print(f"{html_check=}")
            gc.collect()
            # memory_usage()

    else:
        ads: list = ads_listed_parser(text, datetime.now(timezone.utc), return_list_of_list_data=True, url=url)
        if ads == ["Invalid page"]:
            return None

        # ad[1] => link
        ad_specific_tasks_collection = (ads_all_details(session, ad[1], connection, start_url) for ad in ads)

        # do first as ad should be inserted first
        # DB operation
        insert_ads(connection, ads)

        # assert len(ads) == len(await asyncio.gather(*ad_specific_tasks_collection))
        await asyncio.gather(*ad_specific_tasks_collection)

        pages += 1

        if pages % 10 == 0:
            connection.commit()
            print(f"{pages=}")
            gc.collect()
            # memory_usage()


async def ads_listed_details(session, url, connection, start_url=None):
    """
    Function ads_listed_details scraps all ads listed in a given url
    """
    async with session.get(url) as response:
        text = await response.text()

    # works fast
    ads: list = ads_listed_parser(text, datetime.now(timezone.utc), return_list_of_list_data=True)
    if ads == ["Invalid page"]:
        return None

    insert_ads(connection, ads)
    # commit is done for every page
    connection.commit()

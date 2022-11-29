import asyncio

from datetime import datetime, timezone

from aiohttp_client import aiohttp_get_request
from insert_data import insert_ads

from ads_listed_parser import ads_listed_parser

from ad_specific_parser import ad_specific_parser_and_insert_db

pages = 0
# ads_count = 0


def debug_response(response_text):
    with open('temp.html', 'w') as f:
        f.write(response_text)


async def ads_all_details(session, url, connection):

    """
    # 20 pages
    # with db insert
    # 32.751898002001326
    # just parsing
    # 21.446617995999986
    """

    global pages

    async with session.get(url) as response:
        text = await response.text()

    if not url.startswith("https://www.funda.nl/koop/heel-nederland/p"):

        # ad_id = 1

        cursor = connection.cursor()
        cursor.execute("SELECT id from ads where link = ?", (url,))
        ad_id = cursor.fetchone()[0]

        ad_specific_parser_and_insert_db(text, ad_id, url, connection)

    else:

        ads: list = ads_listed_parser(text, datetime.now(timezone.utc), return_list_of_list_data=True, url=url)
        # ad[1] => link
        ad_specific_tasks_collection = (ads_all_details(session, ad[1], connection) for ad in ads)

        # do first as ad should be inserted first
        # DB operation
        insert_ads(connection, ads)

        await asyncio.gather(*ad_specific_tasks_collection)

        pages += 1
        if pages % 100 == 0:
            print(pages)


async def ads_listed_details(session, url, connection=None):

    text = await aiohttp_get_request(session, url)
    # works fast
    ads: list = ads_listed_parser(text, datetime.now(timezone.utc), return_list_of_list_data=True)
    insert_ads(connection, ads)

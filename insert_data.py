import sqlite3


def insert_html_string(cursor, ad_id, html_string):
    QUERY_RAW_HTML_TEXT = "INSERT INTO ad_details(ad_id, ad_body) VALUES(?, ?)"

    try:
        cursor.execute(QUERY_RAW_HTML_TEXT, (ad_id, html_string))
    except sqlite3.IntegrityError:
        pass


def insert_images(cursor, images_list):
    QUERY_IMAGES = "INSERT INTO images(ad_id, type_of_image, image_link) VALUES(?, ?, ?)"

    try:
        cursor.executemany(QUERY_IMAGES, images_list)
    except sqlite3.IntegrityError:
        pass


def update_ads_coordinates(cursor, ad_id, coordinates):
    QUERY_COORDINATES = "UPDATE ads SET latitude=?, longitude=?, error_link=? WHERE id=?"
    cursor.execute(QUERY_COORDINATES, coordinates + [ad_id])


def insert_ads_old(connection, ads_list):
    # ::'list of dict'::

    cursor = connection.cursor()
    QUERY = """
                INSERT INTO ads(status, link, thumbnail_link, name, address, price, living_space, plot_area, rooms, broker_name, broker_link, type, added_on)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(link)
                DO UPDATE SET status=excluded.status, link=excluded.link, thumbnail_link=excluded.thumbnail_link, name=excluded.name, address=excluded.address, price=excluded.price, living_space=excluded.living_space, plot_area=excluded.plot_area, rooms=excluded.rooms, broker_name=excluded.broker_name, broker_link=excluded.broker_link, type=excluded.type
                RETURNING id, link;
            """

    result = []
    for ad in ads_list:
        cursor.execute(QUERY, list(ad.values()))
        result += [cursor.fetchone()]

    return result


def insert_ads(connection, ads_list):
    # ::'list of list'::
    cursor = connection.cursor()
    QUERY = """
                INSERT INTO ads(status, link, thumbnail_link, name, address, price, living_space, plot_area, rooms, broker_name, broker_link, type, added_on)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(link)
                DO NOTHING
                """

    cursor.executemany(QUERY, ads_list)


def insert_ad_specific_details(connection, ad_id, html_string, images_list, coordinates):
    cursor = connection.cursor()

    insert_html_string(cursor, ad_id, html_string)
    update_ads_coordinates(cursor, ad_id, coordinates)
    insert_images(cursor, images_list)

import json

from bs4 import BeautifulSoup
from get_best_image import get_best_image_source_str
from insert_data import insert_ad_specific_details

import zlib


def ad_specific_parser_and_insert_db(html_doc, ad_id, url=None, connection=None):
    soup = BeautifulSoup(html_doc, "lxml")
    soup = soup.body

    html_string = html_doc
    # compressing step
    html_string = html_doc.encode()
    html_compress = zlib.compress(html_string)
    html_string = html_compress

    # decompressing step
    # html_string = zlib.decompress(html_string).decode()
    # print(html_string==html_doc)

    images_list = image_links_new(soup, ad_id)
    coordinates = get_coordinates(soup, url)

    # DB operation
    insert_ad_specific_details(connection, ad_id, html_string, images_list, coordinates)


def image_links_new(soup, ad_id):
    # root_link = "https://www.funda.nl"
    media = []

    photos = soup.find("div", id="overview-photos")
    if photos:
        for i in photos.find_all("img", "media-viewer-overview__section-image"):
            media.append([ad_id, "overview-photos", get_best_image_source_str(i)])

    floorplan = soup.find("div", id="overview-floorplan")
    if floorplan:
        for i in floorplan.find_all("img", "media-viewer-overview__section-image"):
            media.append([ad_id, "overview-floorplan", get_best_image_source_str(i)])

    photo_360_views = soup.find("div", id="overview-360photos")
    if photo_360_views:
        for i in photo_360_views.find_all("img", "media-viewer-overview__section-image"):
            media.append([ad_id, "overview-360photos", get_best_image_source_str(i)])

    return media


def get_coordinates(soup, url=None, covert_to_soup=False):
    if covert_to_soup:
        soup = BeautifulSoup(soup, "lxml")
        soup = soup.body

    try:
        coordinates_json_string = soup.select("script[data-media-viewer-map-config='']")[0]
    except Exception as error:
        error = f"link expired or wrong link - {error}"
        return [None, None, error]
    else:
        coordinates = json.loads(coordinates_json_string.string)
        try:
            lat: str = coordinates["lat"] or None
            long: str = coordinates["lat"] or None
        except KeyError as error:
            print(coordinates)
            error = f"link expired or wrong link - {error}"
            return [None, None, error]
        else:
            return [lat, long, None]

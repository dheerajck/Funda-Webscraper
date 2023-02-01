import sys
import re

from bs4 import BeautifulSoup

from get_best_image import get_best_image_source_str


def remove_newline(text):
    # return text.replace("\n", " ").strip()

    if text is not None:
        try:
            return re.sub(r"(\W+)", " ", text)
        except Exception as error:
            print(f"{text} - {error}")
            sys.exit()
    else:
        return None


def extract_int(text):
    try:
        return int(re.sub("[^0-9]", "", text))
    except Exception:
        return None


def image_download(name, link):
    """
    save image in a folder
    """


def get_all_images(ad_link):
    """
    get all images
    """


def get_text(bs4tag):
    # bs4tag.text or soup.get_text()
    if bs4tag is None:
        return ""
    else:
        return bs4tag.get_text(strip=True)


######################################################################################################################


def get_listed_ads(ad, added_time_test):
    data = {
        "status": None,
        "link": None,
        "thumbnail_link": None,
        "name": None,
        "address": None,
        "price": None,
        "living_space": None,
        "plot_area": None,
        "rooms": None,
        "broker_name": None,
        "broker_link": None,
        "type": None,
        "added_on": None,
    }

    root_link = "https://www.funda.nl"

    # first part
    search_result_thumbnail_container = ad.find("div", "search-result-thumbnail-container")

    status = get_text(search_result_thumbnail_container.li)
    status = get_text(search_result_thumbnail_container.li)
    data["status"] = remove_newline(status) or None

    thumbnail_link = search_result_thumbnail_container.img.get("src")
    data["thumbnail_link"] = thumbnail_link or None

    # second part
    search_result_content = ad.find("div", "search-result-content")
    name_address = search_result_content.find("div", "search-result__header-title-col")
    first_a_tag_link = name_address.a["href"]  # relative link
    first_a_tag_link = root_link + first_a_tag_link  # absolute link
    data["link"] = first_a_tag_link or None

    ad_name = get_text(search_result_content.find("h2", "search-result__header-title fd-m-none"))
    data["name"] = remove_newline(ad_name) or None

    ad_address = get_text(search_result_content.find("h4", "search-result__header-subtitle fd-m-none"))
    data["address"] = remove_newline(ad_address) or None

    price = get_text(ad.find("span", "search-result-price"))
    data["price"] = extract_int(price) or None

    usable_area_of_living = get_text(ad.find("span", title="Gebruiksoppervlakte wonen"))
    data["living_space"] = extract_int(usable_area_of_living) or None

    plot_area = get_text(ad.find("span", title="Perceeloppervlakte"))
    data["plot_area"] = extract_int(plot_area) or None

    # match-just-one-and-only-one-css-class
    rooms = ad.select("div[class='search-result-info']")[0].find_all("li")
    if (len(rooms) > 0) and (rooms := get_text(rooms[-1])):
        if "kamer" not in rooms:
            rooms = None
    else:
        rooms = None

    data["rooms"] = extract_int(rooms) or None

    broker = ad.find("a", "search-result-makelaar")
    broker_link = broker["href"]
    broker_link = root_link + broker_link
    data["broker_link"] = broker_link or None

    broker_name = get_text(broker.find("span", "search-result-makelaar-name"))
    data["broker_name"] = remove_newline(broker_name) or None

    if added_time_test is not None:
        data["added_on"] = added_time_test

    data["type"] = "main"

    # if data["name"] is None:
    #     print("ip ban")
    #     sys.exit()

    return data


######################################################################################################################


def get_promo_ads(ad, added_time_test):
    data = {
        "status": None,
        "link": None,
        "thumbnail_link": None,
        "name": None,
        "address": None,
        "price": None,
        "living_space": None,
        "plot_area": None,
        "rooms": None,
        "broker_name": None,
        "broker_link": None,
        "type": None,
        "added_on": None,
    }

    root_link = "https://www.funda.nl"

    search_result_thumbnail_container = ad.find("div", "search-result-image-promo")

    thumbnail_link = get_best_image_source_str(search_result_thumbnail_container.find("img"))
    data["thumbnail_link"] = thumbnail_link or None

    status = get_text(search_result_thumbnail_container.li)
    status = get_text(search_result_thumbnail_container.li)
    data["status"] = remove_newline(status) or None

    # second part
    search_result_content = ad.find("div", "search-result-content-promo")
    # search_result_content_child_ = ad.find("div", "search-result-content-info")

    name_address = search_result_content.find("div", "search-result__header-title-col")
    first_a_tag_link = name_address.a["href"]  # relative link
    first_a_tag_link = root_link + first_a_tag_link  # absolute link
    data["link"] = first_a_tag_link or None

    ad_name = get_text(search_result_content.find("h2", "search-result__header-title fd-m-none"))
    data["name"] = remove_newline(ad_name) or None

    ad_address = get_text(search_result_content.find("h4", "search-result__header-subtitle fd-m-none"))
    data["address"] = remove_newline(ad_address) or None

    price = get_text(ad.find("span", "search-result-price"))
    data["price"] = extract_int(price) or None

    usable_area_of_living = get_text(ad.find("span", title="Gebruiksoppervlakte wonen"))
    data["living_space"] = extract_int(usable_area_of_living) or None

    plot_area = get_text(ad.find("span", title="Perceeloppervlakte"))
    data["plot_area"] = extract_int(plot_area) or None

    rooms = ad.select("div[class='search-result-info']")[0].find_all("li")
    if (len(rooms) > 0) and (rooms := get_text(rooms[-1])):
        if "kamer" not in rooms:
            rooms = None
    else:
        rooms = None

    data["rooms"] = extract_int(rooms) or None

    broker = ad.find("a", "search-result-makelaar")

    if broker is None:
        # structure change
        # data stored in div now

        # a tag with same name inside div
        broker = ad.find("div", "search-result-makelaar").find("a", "search-result-makelaar-name")

        broker_link = broker["href"]
        broker_link = root_link + broker_link

        # name is not included in span, its in a tag
        broker_name = get_text(broker)

    else:
        broker_link = broker["href"]
        broker_link = root_link + broker_link

        broker_name = get_text(broker.find("span", "search-result-makelaar-name"))

    # updating broker link, broker name
    data["broker_link"] = broker_link or None
    data["broker_name"] = remove_newline(broker_name) or None

    if added_time_test is not None:
        data["added_on"] = added_time_test

    data["type"] = "promo"

    return data


######################################################################################################################


def ads_listed_parser(html_doc, added_time_test=None, return_list_of_list_data=None, url=None):
    soup = BeautifulSoup(html_doc, "lxml")
    pagecheck = soup.find(string="0 resultaten")
    if pagecheck:
        return ["Invalid page"]

    # print(soup.title.text)
    if soup.title.text.strip() == "Je bent bijna op de pagina die je zoekt [funda]":
        print("bot detected")
        sys.exit()
    soup = soup.body

    cleaned_ads_in_this_page: list = []

    # collects main ads
    list_of_ads = soup.find_all("div", "search-result-main")

    if len(list_of_ads) == 0:
        print("no ads in list, bot => ip and user agent", url)
        sys.exit()

    for ad in list_of_ads:
        data: dict = get_listed_ads(ad, added_time_test)
        if return_list_of_list_data:
            data = list(data.values())
        cleaned_ads_in_this_page.append(data)

    # __________________________________________________________

    # collects promotion ads
    list_of_promoads = soup.find_all("div", "search-result-main-promo")

    for ad in list_of_promoads:
        data: dict = get_promo_ads(ad, added_time_test)
        if return_list_of_list_data:
            data = list(data.values())
        cleaned_ads_in_this_page.append(data)

    return cleaned_ads_in_this_page

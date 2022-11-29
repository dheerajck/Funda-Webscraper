import requests
from bs4 import BeautifulSoup


def get_total_pages(url):
    """
    get the final page number that exist now
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive',
    }

    response = requests.get(url, headers=headers)
    # print("done")

    soup = BeautifulSoup(response.text, "lxml")

    pages_present = soup.find("div", "pagination-pages").find_all("a")
    final_page_number: str = pages_present[-1]["data-pagination-page"]
    final_page_number = int(final_page_number)

    return final_page_number


if __name__ == "__main__":
    get_total_pages("https://www.funda.nl/koop/heel-nederland/")

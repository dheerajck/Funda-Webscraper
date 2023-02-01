import asyncio
import aiohttp


def aiohttp_client():
    # reuse session
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
    #     'Accept-Encoding': 'gzip, deflate',
    #     'Accept': '*/*',
    #     'Connection': 'keep-alive',
    # }

    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Mobile Safari/537.36",
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        "referer": "https://www.funda.nl/",
        'Connection': 'keep-alive',
    }

    my_timeout = aiohttp.ClientTimeout(
        total=None,  # default value is 5 minutes, set to `None` for unlimited timeout
        sock_connect=None,  # How long to wait before an open socket allowed to connect
        sock_read=None,  # How long to wait with no data being read before timing out
    )
    conn = aiohttp.TCPConnector(limit=100, use_dns_cache=False, force_close=False)
    session = aiohttp.ClientSession(headers=headers, timeout=my_timeout, connector=conn)
    return session


async def aiohttp_get_request(session, url):
    async with session.get(url) as response:
        # print(response.headers)
        # response.status, response.headers, await response.text()
        return await response.text()


async def aiohttp_testing_ip_address():
    session = aiohttp_client()
    async with session:
        # _, _, text = await aiohttp_get_request(session, "http://jsonip.com")
        text = await aiohttp_get_request(session, "http://jsonip.com")
        print(text)


def debug_response(response_text):
    # easy_test_response
    with open('temp.html', 'w') as f:
        f.write(response_text)


if __name__ == "__main__":
    asyncio.run(aiohttp_testing_ip_address())

import asyncio
import aiohttp


async def get_ipaddress():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive',
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get('http://jsonip.com', headers=headers) as response:
            json_response = await response.json()
            print(json_response)


if __name__ == "__main__":
    asyncio.run(get_ipaddress())

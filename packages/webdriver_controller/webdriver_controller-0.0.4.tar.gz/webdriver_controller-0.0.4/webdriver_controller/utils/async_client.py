import asyncio
from typing import List

import aiohttp
import async_timeout

from webdriver_controller import config

CHUNK_SIZE = 1024
DOWNLOAD_TIMEOUT = 300


async def fetch(session: aiohttp.ClientSession, url: str):
    print('download {} ...'.format(url))
    file_path = '{}/{}'.format(config.INSTALLATION_FOLDER,
                               url[(url.rfind('/') + 1):])
    with async_timeout.timeout(DOWNLOAD_TIMEOUT):
        async with session.get(url) as response:
            if response.status != 200:
                response.raise_for_status()

            with open(file_path, 'wb') as fh:
                while True:
                    chunk = await response.content.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    fh.write(chunk)
            return await response.release()


async def download_coroutine(event_loop, url_list: List[str]):
    async with aiohttp.ClientSession(loop=event_loop) as session:
        tasks = [fetch(session, url) for url in url_list]
        await asyncio.gather(*tasks)


def download(url_list: List[str]):
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(download_coroutine(event_loop, url_list))
    finally:
        event_loop.close()

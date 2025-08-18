import asyncio
import os
import urllib

import aiohttp
from dotenv import load_dotenv

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'

load_dotenv()
DISK_TOKEN = os.environ.get('DISK_TOKEN')
AUTH_HEADERS = {'Authorization': f'OAuth {DISK_TOKEN}'}


async def async_upload_files_to_yandex_disk(files):
    if files is not None:
        tasks = []
        async with aiohttp.ClientSession() as session:
            for file in files:
                tasks.append(
                    asyncio.ensure_future(
                        upload_file_and_get_url(session, file)
                    )
                )
            urls = await asyncio.gather(*tasks)
        result = {}
        for url_dict in urls:
            result.update(url_dict)
        return result


async def upload_file_and_get_url(session, file):
    # Получаем URL для загрузки файла
    payload = {
        'path': f'app:/{file.filename}',
        'overwrite': 'True'
    }
    async with session.get(
        REQUEST_UPLOAD_URL,
        headers=AUTH_HEADERS,
        params=payload
    ) as response:
        data = await response.json()
        upload_url = data['href']
    # Загружаем файл на полученный URL
    async with session.put(
        upload_url,
        data=file.read()  # Читаем файл асинхронно
    ) as response:
        # Получаем Location из заголовков
        location = response.headers['Location']
        location = urllib.parse.unquote(location)
        location = location.replace('/disk', '')
    # Получаем публичную ссылку на файл
    async with session.get(
        DOWNLOAD_LINK_URL,
        headers=AUTH_HEADERS,
        params={'path': location}
    ) as response:
        data = await response.json()
        return {file.filename: data['href']}

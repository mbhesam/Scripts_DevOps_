# SuperFastPython.com
# example of pinging the status of a set of websites
from urllib.request import urlopen
from urllib.error import URLError
from urllib.error import HTTPError
from http import HTTPStatus
import time
import sys
import telegram
import asyncio
import environ

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env('.env.check_status')
BOT_TOKEN = env('BOT_TOKEN')
CHAT_ID = env('CHAT_ID')
TIMEOUT = env.int('TIMEOUT')

def get_website_status(url):
    # handle connection errors
    try:
        # open a connection to the server with a timeout
        with urlopen(url, timeout=TIMEOUT) as connection:
            # get the response code, e.g. 200
            code = connection.getcode()
            return code
    except HTTPError as e:
        return e.code
    except URLError as e:
        return e.reason

# interpret an HTTP response code into a status
def get_status(code):
    if code == HTTPStatus.OK:
        return 'OK'
    return 'ERROR'

# check status of a list of websites
async def check_status_urls(*args):
    for url in args[0]:
        # get the status for the website
        start = time.time()
        code = get_website_status(url)
        # interpret the status
        status = get_status(code)
        end = time.time()
        del_time = end - start
        del_time = round(del_time,2)
        # report status
        message = f'{url:20s}\t: {status:5s}\t{code}\t{del_time}s'
        if status != "OK" or del_time > 20:
            bot = telegram.Bot(token=BOT_TOKEN)
            await bot.send_message(chat_id=CHAT_ID, text=message, read_timeout=120, write_timeout=120, connect_timeout=120,
                               pool_timeout=120)

# list of urls to check
if __name__ == '__main__':
    args = sys.argv[1:]
    async def alert():
        tasks = []
        tasks.append(check_status_urls(args))
        await asyncio.gather(*tasks)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(alert())

# usage: proxychains /var/www/check_status/venv/bin/python /var/www/check_status/check.py https://alkhazanah.com https://ketabpedia.com https://ketablink.com https://best-kutub.com https://almakhtutat.com https://lib2.ketablink.com https://api.ketablink.com https://down.ketabpedia.com
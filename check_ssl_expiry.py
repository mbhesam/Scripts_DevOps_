import sys
import multiprocessing
import ssl
import socket
import datetime
import concurrent.futures
import math
import sys
import telegram
import asyncio
import environ

env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env('.env.check_ssl_expiry')
BOT_TOKEN = env('BOT_TOKEN')
CHAT_ID = env('CHAT_ID')
DEFAULT_HTTPS_PORT = env.int('DEFAULT_HTTPS_PORT')
WORKER_THREAD_COUNT = multiprocessing.cpu_count()
SOCKET_CONNECTION_TIMEOUT_SECONDS = env.int('SOCKET_CONNECTION_TIMEOUT_SECONDS')
WARN_IF_DAYS_LESS_THAN = env.int('WARN_IF_DAYS_LESS_THAN')
EXIT_SUCCESS = 0
EXIT_EXPIRING_SOON = 1
EXIT_ERROR = 2
EXIT_NO_HOST_LIST = 9

def make_host_port_pair(endpoint):
    host, _, specified_port = endpoint.partition(':')
    port = int(specified_port or DEFAULT_HTTPS_PORT)

    return host, port

def pluralise(singular, count):
    return '{} {}{}'.format(count, singular, '' if count == 1 else 's')

def get_certificate_expiry_date_time(context, host, port):
    with socket.create_connection((host, port), SOCKET_CONNECTION_TIMEOUT_SECONDS) as tcp_socket:
        with context.wrap_socket(tcp_socket, server_hostname=host) as ssl_socket:
            # certificate_info is a dict with lots of information about the certificate
            certificate_info = ssl_socket.getpeercert()
            exp_date_text = certificate_info['notAfter']
            # date format is like 'Sep  9 12:00:00 2016 GMT'
            return datetime.datetime.strptime(exp_date_text, r'%b %d %H:%M:%S %Y %Z')


def format_time_remaining(time_remaining):
    day_count = time_remaining.days

    if day_count >= WARN_IF_DAYS_LESS_THAN:
        return pluralise('day', day_count)

    else:
        seconds_per_minute = 60
        seconds_per_hour = seconds_per_minute * 60
        seconds_unaccounted_for = time_remaining.seconds

        hours = int(seconds_unaccounted_for / seconds_per_hour)
        seconds_unaccounted_for -= hours * seconds_per_hour

        minutes = int(seconds_unaccounted_for / seconds_per_minute)

        return '{} {} {}'.format(
            pluralise('day', day_count),
            pluralise('hour', hours),
            pluralise('min', minutes)
        )

def get_exit_code(err_count, min_days):
    code = EXIT_SUCCESS

    if err_count:
        code += EXIT_ERROR

    if min_days < WARN_IF_DAYS_LESS_THAN:
        code += EXIT_EXPIRING_SOON

    return code

def format_host_port(host, port):
    return host + ('' if port == DEFAULT_HTTPS_PORT else ':{}'.format(port))

async def check_certificates(endpoints):
    context = ssl.create_default_context()
    host_port_pairs = [make_host_port_pair(endpoint) for endpoint in endpoints]

    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKER_THREAD_COUNT) as executor:
        futures = {
            executor.submit(get_certificate_expiry_date_time, context, host, port):
            (host, port) for host, port in host_port_pairs
        }

        endpoint_count = len(endpoints)
        err_count = 0
        min_days = math.inf
        max_host_port_len = max([len(format_host_port(host, port)) for host, port in host_port_pairs])
        print('Checking {}...'.format(pluralise('endpoint', endpoint_count)))
        for future in concurrent.futures.as_completed(futures):
            host, port = futures[future]
            try:
                expiry_time = future.result()
            except Exception as ex:
                err_count += 1
                message = '{} ERROR {}'.format(format_host_port(host, port).ljust(max_host_port_len), ex)
                bot = telegram.Bot(token=BOT_TOKEN)
                await bot.send_message(chat_id=CHAT_ID, text=message, read_timeout=120, write_timeout=120,
                                       connect_timeout=120,
                                       pool_timeout=120)
            else:
                time_remaining = expiry_time - datetime.datetime.utcnow()
                time_remaining_txt = format_time_remaining(time_remaining)
                days_remaining = time_remaining.days
                min_days = min(min_days, days_remaining)

                message = ('{} {:<5} expires in {}'.format(
                    format_host_port(host, port).ljust(max_host_port_len),
                    'WARN' if days_remaining < WARN_IF_DAYS_LESS_THAN else 'OK',
                    time_remaining_txt))

                if 'WARN' not in message:
                    bot = telegram.Bot(token=BOT_TOKEN)
                    await bot.send_message(chat_id=CHAT_ID, text=message, read_timeout=120, write_timeout=120,
                                           connect_timeout=120,
                                           pool_timeout=120)


    exit_code = get_exit_code(err_count, min_days)
    sys.exit(exit_code)

if __name__ == '__main__':
    endpoints = sys.argv[1:]

    if len(endpoints):
        async def alert():
            tasks = []
            tasks.append(check_certificates(endpoints))
            await asyncio.gather(*tasks)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(alert())
    else:
        print('Usage: {} <list of endpoints>'.format(sys.argv[0]))
        sys.exit(EXIT_NO_HOST_LIST)

# usage: proxychains /var/www/check_ssl/venv/bin/python /var/www/check_ssl/check_ssl_expiry.py alkhazanah.com ketabpedia.com www.ketablink.com best-kutub.com almakhtutat.com lib2.ketablink.com api.ketablink.com down.ketabpedia.com

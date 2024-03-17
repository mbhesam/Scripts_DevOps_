import os
import re
import requests
from datetime import datetime, timedelta
from socket import gethostname
import subprocess

HOSTNAME = gethostname()
# Replace with your actual Telegram bot token and chat ID
def check_200(log_file_path):
    tail_command = ['tail','-n','30', log_file_path]
    process = subprocess.Popen(tail_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out_put = process.stdout.readline().decode()
    search_result = re.search(" 20. (HIT|MISS) ",out_put)
    if search_result == None:
        return True
    else:
        return False
def send_telegram_alert(message):
    url = 'TELEPUSH_URL'
    body = {
        'text': message
    }
    res = requests.post(url, json=body, timeout=15)
    res.raise_for_status()
    return True

def check_log_file(log_file_path,site_name):
    # Get the last modified time of the log file
    log_modified_time = os.path.getmtime(log_file_path)
    last_modified = datetime.fromtimestamp(log_modified_time)

    # Calculate the time difference between now and the last modified time
    time_diff = datetime.now() - last_modified

    # Define the threshold time interval (15 minutes in this example)
    threshold = timedelta(minutes=15)
    message = f"{site_name} on cache server {HOSTNAME} has not 200 status code for a quarter"
    if time_diff > threshold:
        # Alert code goes here (send email, notification, etc.)
        send_telegram_alert(message)
    else:
        has_200 = check_200(log_file_path)
        if has_200 == False:
            send_telegram_alert(message=message)
        else:
            pass

if __name__=='__main__':
    SITE_LIST = ["WEBSITES_LIST"]

    for site in SITE_LIST:
        log_file_path = f"/var/log/nginx/{site}-access.log"
        # Call the function to check the log file
        check_log_file(log_file_path,site)

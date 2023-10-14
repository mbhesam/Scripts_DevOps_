import telegram
import asyncio
import time
import os
import re
import socket
from datetime import datetime
import environ

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env('.env.check_status')
BOT_TOKEN = env('BOT_TOKEN')
CHAT_ID = env('CHAT_ID')

# Create the dictionary you can add more groups in .env and in this dictionary
SENSETIVE_WORDS = {
    'GROUP1': env.list('GROUP1', default=[]),
    'GROUP2': env.list('GROUP2', default=[])
}

# define func to return hostname
def get_hostname():
    hostname = socket.gethostname()
    return hostname

def follow(thefile):
    '''generator function that yields new lines in a file
    '''
    # seek the end of the file
    thefile.seek(0, os.SEEK_END)
    # start infinite loop
    while True:
        # read last line of file
        line = thefile.read()        # sleep if file hasn't been updated
        if not line:
            time.sleep(2)
            continue
        yield line

async def check_command(log_command,sensetive_words):
    for word in sensetive_words:
        if word in log_command:
            username_pattern = r'(AUID)="([^"]+)"'
            username_matches = re.findall(username_pattern, log_command)
            username = "".join(list(set([match[1] for match in username_matches])))
            command_pattern = r'(a\d)="([^"]+)"'
            command_matches = re.findall(command_pattern, log_command)
            command = " ".join([match[1] for match in command_matches])
            hostname = get_hostname()
            now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            message = now+" *** "+username+" *** "+command+" *** "+hostname
            bot = telegram.Bot(token=BOT_TOKEN)
            # Send the message to the Telegram group
            await bot.send_message(chat_id=CHAT_ID, text=message,read_timeout=120,write_timeout=120,connect_timeout=120 ,pool_timeout=120)
    
if __name__=='__main__':
    async def main():
        tasks = []
        logfile = open("/var/log/audit/audit.log","r")
        loglines = follow(logfile)   
        for log_command in loglines:
            groupname_pattern = r'(EGID)="([^"]+)"'
            groupname_matches = re.findall(groupname_pattern, log_command)
            groupname = "".join(list(set([match[1] for match in groupname_matches]))) 
            try:
                sensetive_words = SENSETIVE_WORDS[groupname]
                tasks.append(check_command(log_command=log_command,sensetive_words=sensetive_words))
                await asyncio.gather(*tasks)
                tasks = []
            except:
                pass
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    

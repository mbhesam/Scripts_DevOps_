import subprocess

def sync_folders(local_folder, remote_folder, remote_ip, remote_username):
    command = f"rsync --size-only  --remove-source-files -avz {local_folder} {remote_username}@{remote_ip}:{remote_folder}"
    subprocess.Popen(command, shell=True)

# Example usage
local_folder = "/root/tg-scraper"
remote_folder = "/gluster/tg-scraper"
remote_ip = "IP"
remote_username = "USERNAME"

while True:
    sync_folders(local_folder, remote_folder, remote_ip, remote_username)

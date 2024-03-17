# create /data directory if does not exists
mkdir -p /data
# calculate date
date=$(date +%Y-%m-%d)
# remove last dump data
rm -f /data/* 
# execute python program with virtual envirnoment  interpreter
venv/bin/python clickhouse-backup/main.py
cd /data
# compress dump data
tar -cvzf "clickhouse-$date.tar.gz" *.tar.gz
sshpass -p '<SCP_PASSWORD>' scp  "clickhouse-$date.tar.gz"  <SCP_USER>@<SCP_IP_ADDRESS>:<SCP_LOCATION>

import datetime
import subprocess
from main import MASTER_CLICKHOUSE_HOST, MASTER_CLICKHOUSE_USER, MASTER_CLICKHOUSE_PASSWORD, SLAVE_CLICKHOUSE_HOST

x = datetime.datetime.now()
date = x.strftime("%Y-%m-%d")
def transfer_data(database,table):
    try:
        backup_command = f"clickhouse-client  --host {MASTER_CLICKHOUSE_HOST} --port 9000 --user {MASTER_CLICKHOUSE_USER} --password '{MASTER_CLICKHOUSE_PASSWORD}' --query 'SELECT * from {database}.{table}' --format TSV > /data/{database}.{table}-{date}.tsv"
        slave_backup_process = subprocess.call(backup_command,shell=True,stdout=subprocess.PIPE, universal_newlines=True)
        exit_code_slave_backup = slave_backup_process
        if exit_code_slave_backup == 0:
            msg_slave_backup = f"SUCCESSFULL BACKUP FOR {database}.{table}"
        else:
            msg_slave_backup = f"ERROR BACKUP WITH EXIT CODE: {exit_code_slave_backup}"
        restore_command = f"clickhouse-client -q 'INSERT INTO {database}.{table} FORMAT TabSeparated' < /data/{database}.{table}.tsv && cd /data/ && tar -czvf  {database}.{table}-{date}.tsv.tar.gz {database}.{table}-{date}.tsv && rm {database}.{table}-{date}.tsv"
        slave_restore_process = subprocess.call(restore_command,shell=True,stdout=subprocess.PIPE, universal_newlines=True)
        exit_code_slave_restore = slave_restore_process.returncode
        if exit_code_slave_restore == 0:
            msg_slave_restore = f"SUCCESSFULL RESTORE ON {SLAVE_CLICKHOUSE_HOST} FOR {database}.{table}"
        else:
            msg_slave_restore = f"ERROR ON {SLAVE_CLICKHOUSE_HOST} WITH EXIT CODE: {exit_code_slave_restore}"
        result_msg = msg_slave_backup + "][" + msg_slave_restore
    except Exception as ex:
        result_msg = f"EXCEPTION EXECUTED FOR {database}.{table}: {ex}"
    return result_msg

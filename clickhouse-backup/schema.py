import logging
import time
import data

logger2 = logging.getLogger('Logger2')
handler2 = logging.FileHandler('logs/script.log', mode='a')
handler2.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] [%(module)s.%(funcName)s:%(lineno)d] %(message)s'))
logger2.addHandler(handler2)
logger2.setLevel(logging.DEBUG)

def transfer_schema(client_master,client_slave):
    result_database = client_master.command("SHOW DATABASES;")
    databases = result_database.split("\n")
    default_dbs = ["default","INFORMATION_SCHEMA","information_schema","system"]
    for db in default_dbs:
        databases.remove(db)
    #print(databases)
    for count_db,database in enumerate(databases):
        client_slave.command(f"create database if not exists {database};")
        client_master.command(f"use {database};")
        # print(f"********{database}********:\n{tables}")
        result_tables = client_master.command(f"SHOW TABLES;")
        tables = result_tables.split("\n")
        for count_tb,table in enumerate(tables):
            if table == "link_request_log" :
                continue
            else:
                client_master.command(f"use {database};")
                result_schema = client_master.command(f"SHOW CREATE TABLE {table.strip()};")
                query_use = f"use {database};"
                query_create = result_schema.replace("\\n"," ").replace('\\','')
                #print(f"********{database}********:\n{table}\n{query_create}")
                try:
                    client_slave.command(query_use)
                    existing_tables = str(client_slave.command("SHOW TABLES;"))
                    if table in existing_tables:
                        logger2.info(f"[slave_deploy: {table}_schema exists already]")
                    else:
                        client_slave.command(query_create)
                        logger2.info(f"[slave_deploy: {table}_schema successfull]")
                except Exception as ex:
                    logger2.info(f"[slave_deploy: {table}_schema_failed: {ex}]")
                try:
                    msg = data.transfer_data(database=database,table=table)
                    print(f"sleep 5 after table {table}")
                    time.sleep(5)
                    logger2.info(f"[slave_deploy: {table}_data successfull][{msg}]")
                except Exception as ex:
                    logger2.info(f"[slave_deploy: {table}_data failed: {ex}]")
    result = "finish job"
    logger2.info(f"[********* {result} ********]")
    return result


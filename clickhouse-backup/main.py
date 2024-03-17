import clickhouse_connect
import environ
import schema

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env('../.env.alert_traffic_elk')

MASTER_CLICKHOUSE_HOST = env("MASTER_CLICKHOUSE_HOST")
MASTER_CLICKHOUSE_USER = env("MASTER_CLICKHOUSE_USER")
MASTER_CLICKHOUSE_PASSWORD = env("MASTER_CLICKHOUSE_PASSWORD")
SLAVE_CLICKHOUSE_HOST = env("SLAVE_CLICKHOUSE_HOST")
SLAVE_CLICKHOUSE_USER = env("SLAVE_CLICKHOUSE_USER")
SLAVE_CLICKHOUSE_PASSWORD = env("SLAVE_CLICKHOUSE_PASSWORD")
client_master = clickhouse_connect.get_client(host=MASTER_CLICKHOUSE_HOST, username=MASTER_CLICKHOUSE_USER, password=MASTER_CLICKHOUSE_PASSWORD)
client_slave = clickhouse_connect.get_client(host=SLAVE_CLICKHOUSE_HOST, username=SLAVE_CLICKHOUSE_USER, password=SLAVE_CLICKHOUSE_PASSWORD)

if __name__=="__main__":
    result = schema.transfer_schema(client_master=client_master,client_slave=client_slave)
    print(result)

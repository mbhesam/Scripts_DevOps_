import datetime
import requests
from elasticsearch import Elasticsearch
import environ

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(".env.alert_traffic_elk")
dt = datetime.datetime.now()
DATE = dt.strftime("%Y-%m-%d")
CURRENT_TIME = datetime.datetime.now().time()
START_TIME = datetime.time(env.list('START_TIME')[0], env.list('START_TIME')[1], 0)
END_TIME = datetime.time(env.list('END_TIME')[0], env.list('END_TIME')[1], 0)
ELASTIC_SEARCH_URL = env('ELASTIC_SEARCH_URL')
INDEX_ALIASES = env.list('INDEX_ALIASES')
TELEPUSH_URL = env('TELEPUSH_URL')
TRAFFIC_RATIO = int(env('MINIMUM_ALLOWED_TREAFFIC_RATIO').strip("%")) / 100

ES = Elasticsearch(ELASTIC_SEARCH_URL)
AGGS = {
    "total_gigabytes": {
      "sum": {
        "field": "bytes_sent",
        "script": {
          "source": "_value / 1024 / 1024 / 1024",
          "lang": "painless"
        }
      }
   }
}
QUERY_YESTERDAY = {
    "range": {
      "@timestamp": {
        "gte": "now-1d-1h",
        "lt": "now-1d"
      }
    }
}
QUERY_TODAY = {
    "range": {
      "@timestamp": {
        "gte": "now-1h",
        "lt": "now"
      }
    }
}
def calculate_traffic_ratio(query_yesterday,query_today,index_alias):
    resp_yesterday = ES.search(index=index_alias,query=query_yesterday,aggs=AGGS)
    resp_today = ES.search(index=index_alias,query=query_today,aggs=AGGS)
    traffic_bw_yesterday = resp_yesterday['aggregations']['total_gigabytes']['value']
    traffic_bw_today = resp_today['aggregations']['total_gigabytes']['value']
    ratio = traffic_bw_today/traffic_bw_yesterday
    return ratio

def send_telegram_alert(message):
    body = {
        'text': message
    }
    res = requests.post(TELEPUSH_URL, json=body, timeout=15)
    res.raise_for_status()

if __name__=="__main__":
    if START_TIME < CURRENT_TIME or CURRENT_TIME < END_TIME:
        for index in INDEX_ALIASES:
            ratio = calculate_traffic_ratio(query_yesterday=QUERY_YESTERDAY,query_today=QUERY_TODAY,index_alias=index)
            message = f"[the traffic of {index} is reduced more than {env('MINIMUM_ALLOWED_TREAFFIC_RATIO')} percent in [{DATE}]]"
            if ratio < TRAFFIC_RATIO :
                send_telegram_alert(message=message)
            else:
                continue

import requests
import json
from io import BytesIO
from minio import Minio
from airflow.hooks.base import BaseHook
from airflow.exceptions import AirflowNotFoundException

BUCKET_NAME = 'stock-market'  # NB: no underscores


def _get_stock_prices(url, symbol, headers):
    # print(url)  # https://query1.finance.yahoo.com/v8/finance/chart/
    # print(symbol)  # AAPL
    # print(headers)  # {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    # print(type(headers))  # <class 'dict'>

    url = f'{url}{symbol}?metrics=high?&interval=1d&range=1y'
    response = requests.get(url, headers=headers)
    return json.dumps(response.json()['chart']['result'][0])


def _get_minio_client():
    minio = BaseHook.get_connection('minio')
    client = Minio(
        # http://host.docker.internal:9000
        endpoint=minio.extra_dejson['endpoint_url'].split('//')[1],
        access_key=minio.login,
        secret_key=minio.password,
        secure=False
    )
    return client


def _store_prices(stock):
    client = _get_minio_client()
    if not client.bucket_exists(BUCKET_NAME):
        client.make_bucket(BUCKET_NAME)

    stock = json.loads(stock)  # convert stock to python object
    symbol = stock['meta']['symbol']

    # convert stock (python object) to 'transmittable_data' json string
    data = json.dumps(stock, ensure_ascii=False).encode('utf8')
    # overwrites former prices.json
    obj_w = client.put_object(
        bucket_name=BUCKET_NAME,
        object_name=f"{symbol}/prices.json",
        data=BytesIO(data),
        length=len(data)
    )

    # print(type(client))  # <class 'minio.api.Minio'>
    # print(client)  # <minio.api.Minio object at 0x7f16bca42c50>
    # print(type(obj_w))  # <class 'minio.helpers.ObjectWriteResult'>
    # print(obj_w)  # <minio.helpers.ObjectWriteResult object at 0x7f16bc5892d0>
    # print(type(obj_w.bucket_name))  # <class 'str'>
    # print(obj_w.bucket_name)  # stock-market

    # Return path to the file
    return f'{obj_w.bucket_name}/{symbol}'

# airflow tasks test stock_market get_formatted_csv 2024-01-01


def _get_formatted_csv(path):
    # path = 'stock-market/AAPL'
    client = _get_minio_client()
    prefix_name = f"{path.split('/')[1]}/formatted_prices/"

    # print(BUCKET_NAME)  # stock-market
    # print(prefix_name)  # aapl/formatted_prices/

    objects = client.list_objects(
        BUCKET_NAME, prefix=prefix_name, recursive=True)

    for obj in objects:
        # print(obj.object_name)  # returns with path ie prefix/filename
        if obj.object_name.endswith(".csv"):
            return obj.object_name

    raise AirflowNotFoundException(
        f"There is no CSV file in s3://{BUCKET_NAME}/{prefix_name}")

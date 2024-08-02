from airflow.decorators import dag, task
from datetime import datetime
from airflow.hooks.base import BaseHook
from airflow.sensors.base import PokeReturnValue
import requests
import json
from airflow.operators.python import PythonOperator
from include.stock_market.tasks import _get_stock_prices, _store_prices, _get_formatted_csv, BUCKET_NAME
from airflow.operators.docker_operator import DockerOperator
from astro import sql as aql
from astro.files import File
from astro.sql.table import Table, Metadata
from airflow.providers.slack.notifications.slack_notifier import SlackNotifier

SYMBOL = 'AAPL'


@dag(
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["stock_market"],
    on_success_callback=SlackNotifier(
        slack_conn_id="slack",
        text="The DAG stock market has succeded",
        channel="airflow"
    ),
    on_failure_callback=SlackNotifier(
        slack_conn_id="slack",
        text="The DAG stock market has failed",
        channel="airflow"
    )

)
def stock_market():
    # airflow tasks test stock_market is_api_available 2024-01-01
    @task.sensor(poke_interval=30, timeout=300, mode='poke')
    def is_api_available() -> PokeReturnValue:
        api = BaseHook.get_connection("stock_api")
        url = f'{api.host}{api.extra_dejson["endpoint"]}'
        response = requests.get(url, headers=api.extra_dejson["headers"])
        # print(type(response))  # <class 'requests.models.Response'>
        # print(response)  # <Response [404]>

        condition = response.json()['finance']['result'] is None

        return PokeReturnValue(is_done=condition, xcom_value=url)

    # airflow tasks test stock_market get_stock_prices 2024-01-01
    get_stock_prices = PythonOperator(
        task_id="get_stock_prices",
        python_callable=_get_stock_prices,
        op_kwargs={
            # "url": "https://query1.finance.yahoo.com/v8/finance/chart/",
            "url": "{{ task_instance.xcom_pull(task_ids='is_api_available') }}",
            "symbol": SYMBOL,
            "headers": BaseHook.get_connection('stock_api').extra_dejson["headers"]
        }
    )

    # airflow tasks test stock_market store_price 2024-01-01
    store_prices = PythonOperator(
        task_id="store_prices",
        python_callable=_store_prices,
        op_kwargs={
            "stock": '{{ task_instance.xcom_pull(task_ids="get_stock_prices") }}'
        }
    )

    # airflow tasks test stock_market format_prices 2024-01-01
    format_prices = DockerOperator(
        task_id="format_prices",
        image="airflow/spark-app",
        container_name="format_prices",
        api_version="auto",
        auto_remove=True,  # removes the container after execution
        docker_url="tcp://docker-proxy:2375",
        # shares the same network with spark-master
        network_mode="container:spark-master",
        tty=True,
        xcom_all=False,  # does not return xcom
        mount_tmp_dir=False,  # does not mount any temporary directory
        environment={
            # "SPARK_APPLICATION_ARGS": 'stock-market/AAPL'
            "SPARK_APPLICATION_ARGS": '{{ task_instance.xcom_pull(task_ids="store_prices") }}'
        }
    )

    # airflow tasks test stock_market get_formatted_csv 2024-01-01
    get_formatted_csv = PythonOperator(
        task_id="get_formatted_csv",
        python_callable=_get_formatted_csv,
        op_kwargs={
            # path: stock-market/AAPL
            "path": '{{ task_instance.xcom_pull(task_ids="store_prices") }}'
        }
    )

    # airflow tasks test stock_market load_to_dw 2024-01-01
    load_to_dw = aql.load_file(
        task_id="load_to_dw",
        input_file=File(  # You have to use string concatenation here
            path=f"s3://{BUCKET_NAME}/" + "{{task_instance.xcom_pull(task_ids='get_formatted_csv')}}", conn_id="minio"
        ),
        output_table=Table(
            name="stock_market",
            conn_id="postgres",
            metadata=Metadata(
                schema='public'
            )
        )
    )

    # create the tasks dependencies
    is_api_available() >> get_stock_prices >> store_prices >> format_prices >> get_formatted_csv >> load_to_dw


# call the dag
stock_market()

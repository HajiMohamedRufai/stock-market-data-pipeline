# Enter into airflow CLI
astro dev bash

# View help page (manual)
airflow --help

# list all dags
airflow dags list

# trigger a dag run, run it now
airflow dags trigger <dag_id>

# pause a dag
airflow dags pause <dag_id>

# unpause a dag, 
airflow dags unpause <dag_id>

# delete a dag
airflow dags delete <dag_id>

# list all tasks in a dag
airflow tasks list <dag_id>

#****************************************************************************************************
# test a task
airflow tasks test <dag_id> <task_id> <execution_date>
airflow tasks test stock_market_v0.1 store_prices 2024-01-01
#****************************************************************************************************
# run a taks
airflow tasks test <dag_id> <task_id> <execution_date>


# backfill command - allows you to run a DAG for a specified date range
airflow dags backfill <dag_id> -s <start_date> -e <end_date>

# start the scheduler
airflow scheduler

# start a worker
airflow celery worker

# check the status of a webserver
airflow webserver

# clear a task, implying it will re-run again
airflow tasks clear -s <start_date> -e <end_date> <dag_id> <task_id>





from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

CSV_PATH = '/opt/airflow/data/data.csv'
TABLE_NAME = 'raw_transactions'

def load_csv_to_postgres(**context):
    import re
    import pandas as pd

    from airflow.utils.log.logging_mixin import LoggingMixin

    log = LoggingMixin().log

    df = pd.read_csv(CSV_PATH, encoding='ISO-8859-1')
    df.columns = [re.sub(r'(?<=[a-z])(?=[A-Z])', '_', col).lower() for col in df.columns]
    df = df.where(pd.notnull(df), None)  # Ganti NaN jadi None
    df["invoice_date"] = pd.to_datetime(df["invoice_date"])  

    pg_hook = PostgresHook(postgres_conn_id="postgres_conn")
    engine = pg_hook.get_sqlalchemy_engine()

    df.to_sql(
        TABLE_NAME,
        engine,
        if_exists="append",     # biarkan grow; kita load incremental
        index=False,
        method="multi",         # batching insert
        chunksize=5_000
    )

    # logging
    log.info("Inserted %d rows into %s", len(df), TABLE_NAME)

# Define DAG
with DAG(
    dag_id="etl_load_csv",
    description="Load Online Retail CSV ke PostgreSQL menggunakan PostgresHook",
    start_date=datetime(2023, 1, 1),
    schedule=None,   # manual / on‑demand
    catchup=False,
    tags=["etl", "postgres", "csv"],
) as dag:

    load_task = PythonOperator(
        task_id="load_csv_to_postgres",
        python_callable=load_csv_to_postgres,
    )

    load_task
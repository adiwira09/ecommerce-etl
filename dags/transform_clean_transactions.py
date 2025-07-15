from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime

TABLE_SRC = 'raw_transactions'
TABLE_DEST = 'clean_transactions'

def transform_and_clean(**context):
    import pandas as pd

    from airflow.utils.log.logging_mixin import LoggingMixin
    from airflow.providers.postgres.hooks.postgres import PostgresHook

    log = LoggingMixin().log

    try:
        log.info("Starting data transformation and cleaning from table: %s", TABLE_SRC)

        pg_hook = PostgresHook(postgres_conn_id="postgres_conn")
        engine = pg_hook.get_sqlalchemy_engine()

        df = pd.read_sql(f"SELECT * FROM {TABLE_SRC}", con=engine)
        log.info("Loaded %d rows from %s", len(df), TABLE_SRC)

        # cleaning data
        df = df.dropna(subset=["customer_id"])  # Hanya baris dengan customer
        df = df[df["quantity"] > 0]             # Buang return
        df = df[df["unit_price"] > 0]           # Valid price
        df["total_price"] = df["quantity"] * df["unit_price"]
        df.drop_duplicates(inplace=True) # drop duplicates

        log.info("Transformed data, now %d rows", len(df))

        # save ke tabel clean
        df.to_sql(
            TABLE_DEST,
            con=engine,
            if_exists="replace",  # replace tiap run
            index=False,
            method="multi",
            chunksize=5_000
        )
        log.info("Transformed data saved to %s", TABLE_DEST)
    except Exception as e:
        log.error("Error during transformation: %s", str(e))
        raise

# DAG setup
with DAG(
    dag_id="transform_clean_transactions",
    description="Transform dan bersihkan data transaksi",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=["transform", "postgres"],
) as dag:

    transform_task = PythonOperator(
        task_id="transform_and_clean",
        python_callable=transform_and_clean,
    )

    transform_task

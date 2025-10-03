import pendulum
import requests
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import dlt

# --- dlt source ---
@dlt.source
def spacedevs_source():
    base_url = "https://ll.thespacedevs.com/2.0.0"

    @dlt.resource(name="launches", write_disposition="replace")
    def get_launches():
        resp = requests.get(f"{base_url}/launch/upcoming", timeout=30)
        yield resp.json()   # includes metadata + results

    @dlt.resource(name="agencies", write_disposition="replace")
    def get_agencies():
        resp = requests.get(f"{base_url}/agencies", timeout=30)
        yield resp.json()

    yield get_launches()
    yield get_agencies()

# --- pipeline runner ---
def run_pipeline():
    pipeline = dlt.pipeline(
        pipeline_name="spacedevs_pipeline",
        destination="duckdb",
        dataset_name="spacedevs_data",
    )
    info = pipeline.run(spacedevs_source())
    print(info)

# --- airflow DAG ---
with DAG(
    dag_id="09_spacedevs_dlt_airflow",
    start_date=pendulum.today("UTC").add(days=-1),
    schedule=None,
    catchup=False,
    tags=["dlt", "airflow", "beginner"],
) as dag:

    ping_api = BashOperator(
        task_id="ping_api",
        bash_command="curl -sI 'https://ll.thespacedevs.com/2.0.0/launch/upcoming' | head -n 1",
    )

    run_dlt_pipeline = PythonOperator(
        task_id="run_dlt_pipeline",
        python_callable=run_pipeline,
    )

    notify = BashOperator(
        task_id="notify",
        bash_command='echo "DLT pipeline completed — check DuckDB for launches & agencies tables."',
    )

    ping_api >> run_dlt_pipeline >> notify

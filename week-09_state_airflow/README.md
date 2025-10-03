Great 🙌 I’ll merge all the explanations + Airflow user creation into a single, polished **Week 9 README.md**. Here’s the full 

# Week 9 — State in dlt + First Steps with Apache Airflow 🚀

Welcome to **Week 9** of our *Learning in Public with dlt* journey!
This week we’ll cover two important things:

1. **State in dlt** — what it is and why it matters.
2. **Bonus: Orchestration with Apache Airflow** — how to run your pipeline inside a workflow manager.

---

## 1. What is State in dlt? 🧠

Think of **state** as your pipeline’s **memory**.

When you run a pipeline multiple times, state helps dlt remember things like:

* Which items have already been loaded.
* The last timestamp or ID processed.
* Small flags or lists used to skip duplicates.

👉 Without state, every run would start from scratch.
👉 With state, runs can be **incremental** — only new data is added.

---

### Example: Skipping duplicates with state

```python
import dlt, requests

@dlt.resource(write_disposition="append")
def players_games(chess_url, player):
    # Each resource has its own "notebook" (state)
    checked_archives = dlt.current.resource_state().setdefault("archives", [])

    archives = ["url1", "url2", "url3"]  # imagine these come from API
    for url in archives:
        if url in checked_archives:
            print(f"skipping {url}")
            continue
        checked_archives.append(url)

        r = requests.get(url)
        r.raise_for_status()
        yield r.json()
```

* **First run** → downloads all archives, saves their IDs in state.
* **Next run** → skips duplicates using the remembered list.

---

### Where is state stored?

* **By default** → in your pipeline’s working directory:
  `~/.dlt/pipelines/<pipeline_name>`.

* **In Airflow or Docker** (where local folders reset often) →
  dlt can also save state inside your **destination**, in a special table called `_dlt_pipeline_state`.

This makes state available across environments, not just on your laptop.

---

### When should you use state?

✅ Use state when:

* You want incremental loads (load “only new stuff”).
* You need to skip duplicates.
* You want to track small configs or lists between runs.

❌ Avoid state when:

* You’d need to remember **millions of items** → better to query your database instead.

---

### Inspecting & Resetting State

Check pipeline state:

```bash
dlt pipeline -v chess_pipeline info
```

Reset state fully (drop tables + state):

```bash
dlt pipeline <pipeline_name> drop --drop-all
```

Reset just one resource:

```bash
dlt pipeline <pipeline_name> drop <resource_name>
```

---

## 2. Bonus: First Steps with Apache Airflow 🎛️

So far, we’ve been running pipelines manually.
But in the real world, we often need to:

* Run them **on a schedule** (every hour, day, week).
* **Chain tasks** (e.g., download → transform → notify).
* Monitor and retry if something fails.

That’s what **Apache Airflow** does.

---

### What is Airflow?

* **Open-source orchestration tool**.
* Uses Python to define workflows, called **DAGs** (Directed Acyclic Graphs).
* Each workflow = a set of **tasks** connected by arrows.

Think of Airflow as a **conductor of an orchestra**:

* Each instrument (task) plays at the right time.
* The conductor ensures the music (workflow) stays in sync.

---

### Our First DAG: dlt + SpaceDevs API

We’ll create a DAG with 3 tasks:

1. **Ping the API** → check it’s alive.
2. **Run the dlt pipeline** → load data into DuckDB.
3. **Notify** → print a message when done.

#### `spacedevs_dlt_dag.py`

```python
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
```



## Running Airflow 

> Works on macOS/Linux/WSL/Codespaces. If you’re in a notebook, open a terminal for these steps.

1. **Create & activate a virtual environment**

```bash
# macOS/Linux/WSL
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

```powershell
# Windows PowerShell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

2. **Install Airflow 2.9.3 (with constraints) — recommended**

```bash
AIRFLOW_VERSION=2.9.3
PYVER=$(python -V | awk '{print $2}' | cut -d. -f1-2)

pip install "apache-airflow==${AIRFLOW_VERSION}" \
  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYVER}.txt"
```

3. **Install the project deps**

```bash
pip install dlt[duckdb] requests
```

4. **Set Airflow’s home to the current folder (no hardcoded paths)**

```bash
export AIRFLOW_HOME="$(pwd)"         # macOS/Linux/WSL
# PowerShell:
# $env:AIRFLOW_HOME = (Get-Location).Path
```

> This keeps Airflow’s database/logs inside *this* week’s folder and avoids machine-specific paths.

5. **Place the DAG where Airflow looks**

```bash
mkdir -p "$AIRFLOW_HOME/dags"
# If your file is in this folder, move/copy it into the dags/ directory:
mv spacedevs_dlt_dag.py "$AIRFLOW_HOME/dags/"
# (Or use cp instead of mv if you prefer to keep a copy.)
```

6. **Initialize the DB and start Airflow**

```bash
python -m airflow db migrate   # or: python -m airflow db init
python -m airflow standalone
```

* Starts webserver + scheduler locally
* Prints **login credentials** (username/password). If you missed them:

```bash
cat "$AIRFLOW_HOME/simple_auth_manager_passwords.json.generated"
```

7. **Open the UI**

* Go to **[http://localhost:8080](http://localhost:8080)**

  * In Codespaces: forward port **8080**
* Log in with the credentials above
* Enable **`09_spacedevs_dlt_airflow`** → Trigger it → watch tasks run (ping → run_dlt_pipeline → notify)

---

## Minimal Repo Structure (commit only what matters) 📂


```
week-09_state_airflow/
│── README.md
│── requirements.txt              # (optional: keep only dlt[duckdb] + requests if you prefer installing Airflow separately)
│── dags/
│   └── spacedevs_dlt_dag.py
│── .gitignore
```


## Learn More about Airflow 📚

* 🔗 [Official Airflow Docs — Getting Started](https://airflow.apache.org/docs/apache-airflow/stable/start.html)

---

✨ This week you learned:

* **State in dlt** → the pipeline’s memory for incremental and duplicate-free runs.
* **Airflow basics** → how to define tasks in a DAG, create a user, and run your first orchestrated pipeline.


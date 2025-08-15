# 🗄️ Week 02 – Loading Data from a SQL Database 🚀

Welcome to Week 2 of the **Data Engineering with dlt** learning series.

---

## ❓ What is dlt?

**dlt (Data Load Tool)** is an open-source Python library that makes it simple to extract data from different sources like:
- REST APIs
- SQL databases
- Cloud storage
- Python objects

…and load it into structured datasets in destinations like:
- DuckDB
- BigQuery
- PostgreSQL
- Databricks and more

It takes care of:
- Inferring and evolving schemas automatically
- Handling nested/JSON data
- Loading data incrementally
- Managing configuration and deployment

✅ dlt is easy to use, flexible, and production-ready — it works locally or with orchestration tools like Airflow, serverless functions, and cloud platforms.

**Official docs:** [https://dlthub.com](https://dlthub.com)

---

## ✅ What You’ll Learn This Week

- How to connect dlt to a SQL database
- How to select and load specific tables
- How to avoid duplicates with `replace`
- Where dlt stores database connection credentials
- How to explore your loaded data

---

## 🔧 Setup Instructions

### 1. Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

This will install:

* `dlt` with DuckDB support
* `pymysql` (to connect to MySQL in this example)

### 3. Add credentials

Edit `.dlt/secrets.toml` and paste:

```toml
[sources.sql_database.credentials]
drivername = "mysql+pymysql"
database   = "Rfam"
password   = ""
username   = "rfamro"
host       = "mysql-rfam-public.ebi.ac.uk"
port       = 4497
```

These are public demo credentials for the **RFam** MySQL database.

### 4. Run the pipeline

```bash
python sql_database_pipeline.py
```

This will:

* Fetch the `family` and `genome` tables from the RFam database
* Load them into a DuckDB file (`sql_to_duckdb_pipeline.duckdb`)

### 5. (Optional) Explore the data with Streamlit

```bash
pip install streamlit
dlt pipeline sql_to_duckdb_pipeline show
```

This opens a simple app to browse and query your data.

---

## 📁 Folder Contents

| File/Folder                | Purpose                                    |
| -------------------------- | ------------------------------------------ |
| `sql_database_pipeline.py` | Main pipeline script                       |
| `requirements.txt`         | Python dependencies                        |
| `.dlt/config.toml`         | Pipeline configuration                     |
| `.dlt/secrets.toml`        | Database credentials (public demo for now) |
| `README.md`                | This documentation file                    |

---

## 🧠 Code Concepts in Use

* **`sql_database`**: dlt’s helper for reading from SQL databases
* **`write_disposition`**:

  * `append`: adds new rows each run (default)
  * `replace`: clears the table before loading new data
* **DuckDB**: a local, file-based database that’s fast and perfect for experiments

---

## 🐍 Code Overview

We use the following code in `sql_database_pipeline.py`:

```python
import dlt
from dlt.sources.sql_database import sql_database

# 1) Select the tables you want
source = sql_database().with_resources("family", "genome")

# 2) Define the pipeline
pipeline = dlt.pipeline(
    pipeline_name="sql_to_duckdb_pipeline",
    destination="duckdb",
    dataset_name="sql_to_duckdb_pipeline_data"
)

# 3) Run the pipeline (default: append)
load_info = pipeline.run(source)

print(load_info)
```

To **replace** data on every run and avoid duplicates:

```python
load_info = pipeline.run(source, write_disposition="replace")
```

---

## 💡 What’s Next?

In Week 3, we’ll load data from a cloud storage or a file system.

📌 Stay updated by following me on  [LinkedIn]([#](https://www.linkedin.com/in/mahadi-nagassou-850a87254/)).

---

**#dlt #dataengineering #python #learninginpublic #etl #opensource #sql #duckdb**

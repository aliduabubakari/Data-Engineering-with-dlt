# Week 8 — Destinations in dlt 📦

Welcome to Week 8 of the *Learning in Public with dlt* series!  

So far, we’ve looked at **sources**, **resources**, and **pipelines**. Now it’s time to focus on **destinations** — the place where your data ends up after extraction and normalization.

In dlt, a **destination** is where dlt maintains schema and loads your data.  
Destinations can be:
- Databases (DuckDB, Postgres, BigQuery, Snowflake…)
- Data lakes or cloud buckets (S3, GCS, Azure)
- Vector stores
- Even filesystems

dlt provides built-in destination modules and lets you configure your own.

---

## 1. Declaring a Destination

You can declare the destination when creating your pipeline.  
There are three equivalent ways to do this:

```python
import dlt

# 1) Shorthand type
pipeline = dlt.pipeline("my_pipeline", destination="duckdb")

# 2) Full factory path
pipeline = dlt.pipeline("my_pipeline", destination="dlt.destinations.duckdb")

# 3) Import the factory directly
from dlt.destinations import duckdb
pipeline = dlt.pipeline("my_pipeline", destination=duckdb())
````

👉 All three create the same DuckDB destination.
Declaring upfront allows dlt to sync pipeline state and prepare schemas compatible with that destination.

---

## 2. Naming Destinations & Passing Parameters

If you use multiple destinations of the same type (dev/staging/prod), give them names.

```python
from dlt.destinations import filesystem
from dlt.sources.credentials import AzureCredentials

creds = AzureCredentials(azure_storage_account_name="production_storage")
fs = filesystem("az://prod-bucket", destination_name="production_az_bucket", credentials=creds)

pipeline = dlt.pipeline("my_pipeline", destination=fs, dataset_name="week8_data")
```

👉 The destination name (`production_az_bucket`) will also appear in traces and load info.
This makes it easier to track environments.

---

## 3. Configuring Destinations

You can configure destinations via:

* `.dlt/config.toml`
* `.dlt/secrets.toml`
* Environment variables

### Example config (TOML)

```toml
[destination.filesystem]
bucket_url = "az://my-bucket"

[destination.production_az_bucket]
bucket_url = "az://prod-bucket"

[destination.production_az_bucket.credentials]
azure_storage_account_name = "dltdata"
azure_storage_account_key = "storage_key"
```

### Example config (environment variables)

```bash
export DESTINATION__FILESYSTEM__BUCKET_URL="az://my-bucket"
export DESTINATION__FILESYSTEM__CREDENTIALS__AZURE_STORAGE_ACCOUNT_NAME="dltdata"
export DESTINATION__FILESYSTEM__CREDENTIALS__AZURE_STORAGE_ACCOUNT_KEY="storage_key"
```

### Passing credentials directly

```python
from dlt.destinations import postgres

# Credentials inline (not recommended for production)
pipeline = dlt.pipeline(
    "my_pipeline",
    destination=postgres(credentials="postgresql://loader:loader@localhost:5432/dlt_data"),
)
```

👉 Best practice: keep credentials in secrets or env variables.

---

## 4. Inspecting Destination Capabilities

Each destination has its own capabilities (e.g., identifier length, file formats, naming conventions).

```python
from dlt.destinations import duckdb, snowflake

duck = duckdb(naming_convention="duck_case", recommended_file_size=120_000)
print(dict(duck.capabilities()))

snow = snowflake(naming_convention="sql_cs_v1")  # case-sensitive mode
print(dict(snow.capabilities()))
```

👉 Capabilities tell dlt what’s possible (e.g., max identifier length, case sensitivity).
You can override some parameters (like naming convention or file size).

---

## 5. Multiple Destinations in One Project

You can configure multiple destinations and select them at runtime.

```toml
[destination.destination_one]   # BigQuery
location = "US"

[destination.destination_one.credentials]
project_id = "project-id"
client_email = "service@project.iam.gserviceaccount.com"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
```

```python
from dlt.common.destination import Destination

bq_dest = Destination.from_reference("bigquery", destination_name="destination_one")
pipeline = dlt.pipeline("multi_dest_pipeline", destination=bq_dest, dataset_name="bq_data")
```

👉 This allows you to maintain multiple configs (e.g., dev vs prod) in one project.

---

## 6. Multi-Stage Extract → Normalize → Load

dlt defers accessing the destination until it’s actually needed.
This means you can **extract** and **normalize** data without destination credentials present.

```python
from dlt.destinations import filesystem

pipe = dlt.pipeline("multi_stage_pipeline", destination="filesystem")

pipe.extract([{"a": 1}, {"a": 2}], table_name="letters")
pipe.normalize()

# Destination accessed here
pipe.load(destination=filesystem(bucket_url="az://my-bucket"))
```

👉 Useful in containerized or multi-process workflows.

---

## 7. Naming Conventions & Case Sensitivity

Different warehouses treat identifiers differently:

* **Redshift/Athena**: lowercase only
* **Snowflake**: supports case-sensitive, defaults to uppercase folding
* **DuckDB**: preserves original casing, case-insensitive
* **BigQuery**: fully case-sensitive

You can control this with `naming_convention`:

```python
from dlt.destinations import snowflake
snow_cs = snowflake(naming_convention="sql_cs_v1")  # case-sensitive schema
```

For systems like MSSQL:

```python
from dlt.destinations import mssql
dest = mssql(has_case_sensitive_identifiers=True, naming_convention="sql_cs_v1")
```

👉 This tells dlt how to interpret identifiers but assumes you configured the DB itself accordingly.

---

## 8. Creating a Custom Destination (Reverse ETL)

You can build your own destination with `@dlt.destination`.
Perfect for reverse ETL use cases (push data back to APIs).

```python
import dlt, requests

@dlt.destination(name="http_push")
def http_sink(items, endpoint: str):
    for row in items:
        requests.post(endpoint, json=row, timeout=10)
    return {"sent": len(list(items))}
```

👉 Example: send pipeline output to a webhook or SaaS tool.

---

## Summary

In Week 8, you learned how to work with **destinations** in dlt:

* Declare destinations in 3 ways
* Name them and pass explicit credentials/parameters
* Configure via TOML, secrets, or env vars
* Inspect and tweak capabilities
* Run extract/normalize without immediate destination access
* Control naming conventions and case sensitivity
* Use multiple destinations in the same project
* Even build your own reverse-ETL sink

👉 Mastering destinations makes your pipelines portable — you can flip from local DuckDB to BigQuery or Snowflake with just a config change.


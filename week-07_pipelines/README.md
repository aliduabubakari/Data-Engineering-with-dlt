# Week 7 — Pipelines in dlt 🚀

Welcome to **Week 7** of the *Learning in Public with dlt* series!  
So far, we’ve looked at sources and resources. Now it’s time to connect the dots with the **pipeline**, which is the *engine room* of dlt.

A pipeline is what moves data from your Python code (sources, resources, lists, generators) into your chosen **destination** (like DuckDB, BigQuery, or Snowflake).  
It keeps track of schemas, manages state, and handles data loading safely.

Think of the pipeline as the **data conveyor belt**:  
- It *extracts* data,  
- *normalizes* it into a schema,  
- and *loads* it into your storage.  

Let’s unpack how pipelines work with examples.

---

## 1. Creating Your First Pipeline

The simplest pipeline just loads a Python list of dictionaries into a database.

```python
import dlt

# create a pipeline
pipeline = dlt.pipeline(
    pipeline_name="simple_pipeline",  # used to identify the pipeline
    destination="duckdb",             # where the data will land
    dataset_name="my_dataset"         # logical grouping of tables
)

# run the pipeline with some data
info = pipeline.run(
    [{"id": 1}, {"id": 2}, {"id": 3}],
    table_name="numbers"
)

print(info)
````

### Explanation

* **`dlt.pipeline(...)`** creates a pipeline object. It also creates a *working directory* under `~/.dlt/pipelines/simple_pipeline` to track state and schema.
* **`pipeline.run([...], table_name="numbers")`** loads data into DuckDB, creating a `numbers` table in the `my_dataset` dataset.
* The `info` object contains metadata about what was extracted, normalized, and loaded.

👉 Result: You now have a DuckDB database with a table containing 3 rows (`id = 1, 2, 3`).

---

## 2. Pipelines Accept Different Data Inputs

Pipelines are flexible — they can run with many input types:

* A **list** of dictionaries
* A **generator function**
* A **resource** (`@dlt.resource`)
* A **source** (`@dlt.source`)

Here’s an example with a generator:

```python
def generate_rows(n):
    for i in range(n):
        yield {"id": i+1}

pipeline = dlt.pipeline(
    pipeline_name="generator_demo",
    destination="duckdb",
    dataset_name="demo_data"
)

info = pipeline.run(generate_rows(5))
print(info)
```

👉 This produces a table with 5 rows (`id = 1..5`).
Notice that we didn’t need to hold all data in memory — generators let you stream large datasets efficiently.

---

## 3. Controlling How Data is Written

The `write_disposition` parameter decides what happens when data already exists in the table:

* **`append`** → always add new rows
* **`replace`** → drop the table and recreate it
* **`merge`** → deduplicate & update rows (requires primary keys or merge keys)

Example:

```python
pipeline.run(
    generate_rows(3),
    table_name="numbers",
    write_disposition="replace"  # overwrite data on each run
)
```

👉 This replaces the entire `numbers` table with fresh data every time.

---

## 4. Pipeline Working Directory

Every pipeline has its own working folder (state, schemas, logs). By default:

```
~/.dlt/pipelines/<pipeline_name>
```

This lets dlt:

* Track schema changes
* Remember incremental state (e.g., last `updated_at` value)
* Recover from errors

Check pipeline info from the CLI:

```bash
dlt pipeline simple_pipeline info
```

---

## 5. Refreshing Data

Sometimes you want to **reset** your data. dlt gives three modes via the `refresh` argument:

* **`drop_sources`** → drop all tables & reset state for the whole source
* **`drop_resources`** → reset only selected resources
* **`drop_data`** → truncate the data but keep the schema

Example:

```python
pipeline.run(my_source(), refresh="drop_sources")
```

👉 This clears everything for that source and reloads fresh data.

---

## 6. Monitoring Pipeline Progress

When working with larger datasets, it’s helpful to see progress.
dlt integrates with progress monitors like `tqdm` or `log`.

```python
pipeline = dlt.pipeline(
    pipeline_name="chess_pipeline",
    destination="duckdb",
    dataset_name="chess_data",
    progress="tqdm"  # show progress bar
)
```

👉 This shows a live progress bar while data loads.

---

## 7. Practical Example with an API (JSONPlaceholder)

Let’s use a real API: [JSONPlaceholder](https://jsonplaceholder.typicode.com).
It provides free fake REST API endpoints for testing.

```python
import dlt
import requests


@dlt.source
def jsonplaceholder():
    """
    Groups multiple endpoints (resources) from the JSONPlaceholder API.
    Each endpoint (posts, comments, users) becomes its own resource.
    """

    base_url = "https://jsonplaceholder.typicode.com"
    endpoints = ["posts", "comments", "users"]

    def get_resource(endpoint):
        url = f"{base_url}/{endpoint}"
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        yield resp.json()

    # Dynamically create a resource for each endpoint
    for endpoint in endpoints:
        yield dlt.resource(get_resource(endpoint), name=endpoint)


def main() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="jsonplaceholder_pipeline",
        destination="duckdb",
        dataset_name="jsonplaceholder_data",
    )

    # Run all grouped resources (posts, comments, users)
    info = pipeline.run(jsonplaceholder())
    print(info)


if __name__ == "__main__":
    main()

```

### What happens here:

1. `posts()` fetches data from the API and yields it.
2. `jsonplaceholder()` groups the resource into a source.
3. The pipeline loads everything into DuckDB.

👉 Check your DuckDB — you’ll find a `posts, comments, users` table with 100 blog posts.

---

## 8. Why Pipelines Matter

Pipelines are more than just “runners”:

* They manage **state** (so you can do incremental loads).
* They handle **schema evolution** automatically.
* They let you scale from local DuckDB to cloud warehouses with a config change.
* They centralize logs, errors, and progress.

This makes them the backbone of everything you do in dlt.

---

## Summary

In Week 7, you learned how pipelines:

* Take different input types (lists, generators, sources, resources).
* Control data writing with `append`, `replace`, and `merge`.
* Track state in working directories.
* Work seamlessly with real APIs like JSONPlaceholder.

👉 Pipelines are the **bridge between your data sources and your destinations**.
They keep your workflows consistent, traceable, and production-ready.

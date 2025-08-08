# 📦 Week 01 – Getting Started with dlt 🚀

Welcome to Week 1 of the **Data Engineering with dlt** learning series.

---

## ❓ What is dlt?

**`dlt` (Data Load Tool)** is an open-source Python library that makes it simple to extract data from messy or complex sources like:
- REST APIs
- SQL databases
- Cloud storage
- Python objects

…and load it into structured datasets in destinations like:
- DuckDB
- BigQuery
- PostgreSQL
- Databricks and more.

It takes care of:
- Schema inference and evolution
- Nested/JSON normalization
- Incremental data loading
- Pipeline configuration and deployment

> ✅ `dlt` is easy to use, flexible, and production-ready — it works locally or in orchestration tools like Airflow, serverless functions, and cloud platforms.

Official docs: [https://dlthub.com](https://dlthub.com)

---

## ✅ What You’ll Learn This Week

- How to install and initialize a `dlt` project
- How to use `rest_api_source` to fetch data from REST APIs
- The difference between `append`, `replace`, and `merge` write strategies
- Where `dlt` stores configs and secrets
- How to explore the loaded data visually

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

### 3. Run the pipeline

```bash
python rest_api_pipeline.py
```

This will:

* Fetch Pokémon, berry, and location data from the PokéAPI
* Load them into a DuckDB database file (`rest_api_pokemon.duckdb`)

### 4. (Optional) Explore the database with Streamlit

```bash
pip install streamlit
dlt pipeline rest_api_pokemon show
```

This opens a simple Streamlit app to inspect and query the ingested data.

---

## 📁 Folder Contents

| File/Folder            | Purpose                                        |
| ---------------------- | ---------------------------------------------- |
| `rest_api_pipeline.py` | Main pipeline script                           |
| `requirements.txt`     | Python dependencies                            |
| `.dlt/config.toml`     | Pipeline configuration                         |
| `.dlt/secrets.toml`    | Secret credentials (optional, currently empty) |
| `README.md`            | This documentation file                        |

---

## 🧠 Code Concepts in Use

* **`rest_api_source`**: dlt's helper to auto-configure REST API loading
* **`write_disposition`**:

  * `replace`: wipes the old data every run (default for most)
  * `merge`: updates records using a primary key (used for Pokémon)
* **DuckDB**: a fast, in-process SQL OLAP database — perfect for dev work

---

## 🐍 Code Overview

We use the following config in `rest_api_pipeline.py`:

```python
pipeline = dlt.pipeline(
    pipeline_name="rest_api_pokemon",
    destination="duckdb",
    dataset_name="rest_api_data"
)

pokemon_api = rest_api_source({
    "client": {
        "base_url": "https://pokeapi.co/api/v2/"
    },
    "resource_defaults": {
        "endpoint": {
            "params": {
                "limit": 1000
            }
        },
        "write_disposition": "replace"
    },
    "resources": [
        {
            "name": "pokemon",
            "primary_key": "name",
            "write_disposition": "merge"
        },
        "berry",
        "location"
    ]
})

pipeline.run(pokemon_api)
```

---

## 💡 What’s Next?

In Week 2, we’ll Load data from a SQL database!

📌 Stay updated by following me on [LinkedIn]([#](https://www.linkedin.com/in/mahadi-nagassou-850a87254/)).

**#dlt #dataengineering #python #learninginpublic #etl #opensource**

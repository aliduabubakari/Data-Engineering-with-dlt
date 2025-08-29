📦 Week 03 – Loading Files from Local or Cloud Storage with dlt 🚀

Welcome to Week 3 of the **"Data Engineering with dlt"** educational series.

This week, we’re shifting gears to one of the most common data engineering tasks:

> ✅ Reading raw files (like CSV, JSONL, or Parquet) from your **local machine** or a **cloud bucket**, and transforming them into clean, structured datasets using `dlt`.

---

## 📚 What You’ll Learn This Week

By the end of this lesson, you’ll be able to:

- Connect to local or cloud-based storage (like Google Cloud Storage)
- Use `dlt.sources.filesystem` to discover and read multiple files at once
- Transform CSV files into clean Python records
- Load your data into **DuckDB** (a local analytics database)
- Add metadata (like filename or path) to your loaded data
- Run your pipeline again — and only load **new or modified** files (incremental load)

---

## 🛠️ Step-by-Step Setup

### 1️⃣ Create a virtual environment (recommended)
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
````

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

Your `requirements.txt` should include:

```txt
dlt[duckdb]
pandas
```

> Optionally add `streamlit` if you want to explore the results visually.

---

## 📂 Folder Contents

| File                     | Purpose                                     |
| ------------------------ | ------------------------------------------- |
| `filesystem_pipeline.py` | Main pipeline loading CSVs from local/cloud |
| `requirements.txt`       | Project dependencies                        |
| `.dlt/config.toml`       | Configuration for your pipeline             |
| `.dlt/secrets.toml`      | Secrets like GCP credentials (if needed)    |
| `README.md`              | You’re reading it now 🙂                    |

---

## 🧠 Key Concepts

### 🔸 `filesystem()`

This dlt helper allows you to:

* List all files in a folder (local or cloud)
* Apply a filter using `file_glob="*.csv"` or similar

### 🔸 `read_csv()`

This transformer parses each file into structured Python records.

### 🔸 `pipeline.run()` with `write_disposition`

How you load data:

* `append`: keep adding new rows
* `replace`: delete existing table and reload
* `merge`: deduplicate using a key
* `incremental`: only load new files or rows

---

## 🐍 Example Pipeline Code

```python
import dlt
from dlt.sources.filesystem import filesystem, read_csv

# 1. List files in local folder or GCS bucket
files = filesystem(
    bucket_url="data/",         # local: use folder path, GCS: use "gs://your-bucket"
    file_glob="*.csv"
)

# 2. Read CSVs and enrich with file name
@dlt.transformer()
def read_csv_with_filename(files):
    import pandas as pd
    for file_obj in files:
        with file_obj.open() as f:
            for df in pd.read_csv(f, chunksize=10000):
                df["source_file"] = file_obj["file_name"]
                yield df.to_dict(orient="records")

# 3. Create a pipeline and run
pipeline = dlt.pipeline(
    pipeline_name="filesystem_pipeline",
    destination="duckdb",
    dataset_name="files_data"
)

load_info = pipeline.run(read_csv_with_filename(files), write_disposition="merge")
print(load_info)
```

---

## 🧪 Run the Pipeline

```bash
python filesystem_pipeline.py
```

Your data will be loaded into `filesystem_pipeline.duckdb` and enriched with metadata.

To view the data visually:

```bash
pip install streamlit
dlt pipeline filesystem_pipeline show
```

---

## ☁️ Want to Use Cloud Storage?

Edit your `.dlt/secrets.toml` like this:

```toml
[sources.filesystem.credentials]
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
project_id = "your-project-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
```

And change the `bucket_url` to:

```python
bucket_url="gs://your-bucket-name"
```

---

## 🧠 Recap: Why This Matters

Loading data from files is **the first step** in most real-world data workflows.

With `dlt`, you can:

* Build pipelines that scale from your laptop to the cloud
* Switch between local dev and production with no code changes
* Add rich metadata, schema inference, and logging for free

---

## 📌 Next Steps

In **Week 4**, we’ll go even further — creating a **custom dlt source** that combines all you’ve learned so far (files + transformations + logic)!

Follow along on [LinkedIn](https://github.com/1997mahadi/Data-Engineering-with-dlt)

---

## 🧵 Share your progress!

If you're learning with us, tag your posts with `#dlt #learninginpublic #dataengineering`

---

\#dlt #duckdb #python #dataengineering #etl #filesystem #opensource #learninginpublic


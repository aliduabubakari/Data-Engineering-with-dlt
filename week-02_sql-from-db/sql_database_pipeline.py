import dlt
from dlt.sources.sql_database import sql_database

# 1) Pick the tables you want (keep it simple)
source = sql_database().with_resources("family", "genome")

# 2) Define the pipeline (name, destination, dataset)
pipeline = dlt.pipeline(
    pipeline_name="sql_to_duckdb_pipeline",
    destination="duckdb",
    dataset_name="sql_to_duckdb_pipeline_data",
)

# 3) Run the pipeline
#    Default = "append" (adds rows on every run)
#    For beginners, keep this as-is. If you see duplicates and
#    want to overwrite the table each time, use the replace line below.
load_info = pipeline.run(source)

# 👉 To overwrite each run instead of appending, use:
# load_info = pipeline.run(source, write_disposition="replace")

print(load_info)
print("Done. Created: sql_to_duckdb_pipeline.duckdb")

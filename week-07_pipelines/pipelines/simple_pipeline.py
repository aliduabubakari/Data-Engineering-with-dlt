# Simple pipeline: load a small Python list into DuckDB
# Creates dataset: my_dataset
# Creates table: numbers

import dlt


def main() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="simple_pipeline",   # used to persist state & schema
        destination="duckdb",              # local file-based database
        dataset_name="my_dataset",         # logical group of tables
    )

    data = [{"id": 1}, {"id": 2}, {"id": 3}]
    info = pipeline.run(data, table_name="numbers")
    print(info)


if __name__ == "__main__":
    main()

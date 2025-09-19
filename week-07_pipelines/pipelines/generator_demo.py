# Demonstrates using a generator as pipeline input
# Creates dataset: demo_data
# Creates table: numbers (replace mode in the second run)

import dlt


def generate_rows(n: int):
    """Stream rows without keeping everything in memory."""
    for i in range(1, n + 1):
        yield {"id": i}


def main() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="generator_demo",
        destination="duckdb",
        dataset_name="demo_data",
    )

    # First run: append 5 rows
    info1 = pipeline.run(generate_rows(5), table_name="numbers", write_disposition="append")
    print("First run (append):")
    print(info1)

    # Second run: replace table content with 3 rows
    info2 = pipeline.run(generate_rows(3), table_name="numbers", write_disposition="replace")
    print("\nSecond run (replace):")
    print(info2)


if __name__ == "__main__":
    main()

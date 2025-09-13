import dlt

# Define a simple resource
@dlt.resource
def users():
    """A simple resource yielding user data as dictionaries."""
    yield [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]

# Group resources into a source
@dlt.source
def simple_source():
    """A source grouping the `users` resource."""
    return [users]

# Define and run the pipeline
if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="simple_demo",
        destination="duckdb",
        dataset_name="demo_data"
    )

    info = pipeline.run(simple_source())
    print(info)

import dlt
import requests

@dlt.resource
def posts():
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    response.raise_for_status()
    yield response.json()

@dlt.resource
def comments():
    response = requests.get("https://jsonplaceholder.typicode.com/comments")
    response.raise_for_status()
    yield response.json()

@dlt.resource
def users():
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    response.raise_for_status()
    yield response.json()

@dlt.source
def jsonplaceholder_source():
    return [posts, comments, users]

pipeline = dlt.pipeline(
    pipeline_name="jsonplaceholder_pipeline",
    destination="duckdb",
    dataset_name="jsonplaceholder_data"
)

info = pipeline.run(jsonplaceholder_source())
print(info)

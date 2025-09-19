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

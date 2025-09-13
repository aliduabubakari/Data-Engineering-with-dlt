import dlt

@dlt.source
def dynamic_blog_source():
    endpoints = {
        "posts": [
            {"id": 1, "title": "Dynamic Post"},
            {"id": 2, "title": "Another Dynamic Post"}
        ],
        "comments": [
            {"id": 201, "post_id": 1, "text": "Dynamic Comment!"}
        ]
    }

    for name, data in endpoints.items():
        yield dlt.resource(data, name=name)

pipeline = dlt.pipeline(
    pipeline_name="dynamic_blog_demo",
    destination="duckdb",
    dataset_name="dynamic_blog_data"
)

info = pipeline.run(dynamic_blog_source())
print(info)

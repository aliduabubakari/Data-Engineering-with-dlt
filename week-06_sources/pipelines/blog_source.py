import dlt

@dlt.resource
def posts():
    yield [
        {"id": 1, "title": "First Post"},
        {"id": 2, "title": "Second Post"}
    ]

@dlt.resource
def comments():
    yield [
        {"id": 101, "post_id": 1, "text": "Great post!"},
        {"id": 102, "post_id": 2, "text": "Thanks for sharing!"}
    ]

@dlt.source
def blog_source():
    return [posts, comments]

pipeline = dlt.pipeline(
    pipeline_name="blog_demo",
    destination="duckdb",
    dataset_name="blog_data"
)

info = pipeline.run(blog_source())
print(info)

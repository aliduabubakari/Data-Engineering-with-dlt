````markdown
# Week 6: Understanding Sources in dlt

Welcome to **Week 6** of the *Learning in Public with dlt* journey!  
So far, we’ve built pipelines, managed incremental loading, and explored schemas. This week, we dive into one of the **core concepts of dlt**: the **Source**.

---

## 🌱 What is a Source?

In dlt, a **source** is a *logical grouping of resources*.  
Think of it as a collection of related data endpoints wrapped together — for example, the *posts*, *comments*, and *users* endpoints from an API.

- A **resource** = a single dataset or endpoint (e.g., `/posts`).
- A **source** = a function decorated with `@dlt.source` that groups one or more resources together.

This makes your pipelines **modular, reusable, and clean**.

---

## ✨ Step 1: A Simple Source Example

Let’s start with the most basic case — loading some Python dictionaries as a resource.

```python
import dlt

# Define a resource (a generator of data)
@dlt.resource
def users():
    yield [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

# Group the resource into a source
@dlt.source
def simple_source():
    return [users]

# Define and run a pipeline
pipeline = dlt.pipeline(
    pipeline_name="simple_demo",
    destination="duckdb",
    dataset_name="demo_data"
)

info = pipeline.run(simple_source())
print(info)
````

👉 Here’s what’s happening:

1. We define a **resource** (`users`) that yields JSON-like objects.
2. We group it inside a **source** (`simple_source`).
3. Running the pipeline automatically creates a `users` table inside **DuckDB**.

---

## ✨ Step 2: Multiple Resources in One Source

Sources get really powerful when you combine multiple resources.

```python
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
```

👉 Result:

* Two resources (`posts` and `comments`) are grouped under `blog_source`.
* Running the pipeline creates **two tables** in DuckDB: `posts` and `comments`.

This shows how one source can organize multiple resources into a single, reusable data module.

---

## ✨ Step 3: Dynamic Sources

What if you want to create resources dynamically (e.g., for multiple API endpoints)?
Here’s how:

```python
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
```

👉 Now:

* The resources (`posts` and `comments`) are **created at runtime**.
* You don’t duplicate code — you just loop through endpoints.

---

## 🌍 Step 4: Using a Real API (JSONPlaceholder)

Let’s fetch real-world data using the [JSONPlaceholder API](https://jsonplaceholder.typicode.com/).
This free API simulates common datasets like posts, comments, and users.

```python
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
```

👉 What happens:

* We define **three resources** (`posts`, `comments`, `users`) that fetch real data.
* Group them into a **source** called `jsonplaceholder_source`.
* Run the pipeline → DuckDB now has **real API tables**.

This shows how easily you can move from toy data to production-like sources.

---

## 🔎 Inspecting & Customizing Sources

Once you define a source, you can interact with its resources:

```python
source = jsonplaceholder_source()

print(source.resources.keys())       # See available resources
print(source.resources.selected.keys())  # See which are selected to load

# Run only selected resources
pipeline.run(source.with_resources("posts", "users"))
```

👉 This lets you **select, filter, and control** which resources you want to load.


## 📦 Repo Structure

```
week-06_sources/
├── pipelines/
│   ├── users.py                   # Simple source with one resource
│   ├── blog_source.py              # Multiple resources (posts + comments)
│   ├── dynamic_blog_source.py      # Dynamic resource creation
│   └── jsonplaceholder_source.py   # Real API example
├── schemas/                        # Holds exported schemas
├── requirements.txt
└── README.md
```

---

## 🎯 Why this matters

* **Organization**: Sources group resources logically.
* **Reusability**: The same source can be reused across projects.
* **Flexibility**: Create resources dynamically, filter them, or limit runs.
* **Practicality**: Works just as well with toy data and real-world APIs.

This week gives you the building blocks to design clean, modular pipelines that scale as your projects grow.

---

Let’s keep building 🚀

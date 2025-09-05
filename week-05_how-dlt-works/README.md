````markdown
# Week 5: How dlt Works — A Beginner-Friendly Guide

Welcome to **Week 5** of the *Learning in Public with dlt* journey!  
In the first four weeks, we were hands-on — building pipelines that fetched data from REST APIs, SQL databases, files, and GitHub.  

This week, we **pause to understand how dlt works under the hood**.  
Think of this as the "theory chapter" 📖: we open the engine of dlt and explain every moving part, step by step.

---

## Why Learn the Theory?

It’s tempting to just keep coding pipelines, but without understanding the principles, it’s like driving a car 🚗 without knowing how the engine, gears, and brakes work. You can go forward — but when problems appear, you’re stuck.  

By the end of this chapter, you will be able to explain:  

> “When I run a dlt pipeline, it extracts data from the source, normalizes it into a schema, and loads it into the destination. Along the way, it manages schema evolution, state, and incremental syncs automatically.”

That’s the foundation of modern **ETL (Extract–Transform–Load)** and **ELT (Extract–Load–Transform)**.

---

## The Big Picture of dlt

dlt takes **data from a source** (like GitHub, PostgreSQL, or even a Python list)  
and moves it into a **destination** (like DuckDB, BigQuery, or a data lake).  

In between, it automatically:  
- figures out the schema,  
- handles incremental updates,  
- merges duplicates,  
- manages secrets,  
- and keeps a record of the pipeline state.  

In other words: **you focus on what data you want, and dlt does the heavy lifting of getting it there safely and efficiently.**

---

## The Three Phases of a Pipeline

Every pipeline in dlt follows **three phases**:

1. **Extract** — grab the raw data.  
2. **Normalize** — organize and reshape it into structured tables.  
3. **Load** — move it into your database or warehouse.

Let’s break these down one by one.

---

### 1. Extract: Collecting the Data

This is the **first step**. Extraction is like going to the market 🛒 and picking up raw groceries (your data).

```python
pipeline.extract(data)
````

* dlt pulls the raw data and stores it in a “load package.”
* Each load package has a unique ID and contains the raw source data.
* You can provide *hints* (e.g., column types, primary keys).
* You can also:

  * filter or map data,
  * obfuscate sensitive fields,
  * or use **incremental cursors** to fetch *only new data*.

👉 Beginners’ note: At this stage, dlt does **not** try to structure or clean your data. It just saves it.

---

### 2. Normalize: Structuring the Data

Next comes **normalization**. Imagine you get home with groceries 🛍️ — now you need to wash, cut, and organize them before putting them away.

```python
pipeline.normalize()
```

Here’s what happens:

* dlt **inspects your raw data**.
* It computes the **schema** (the blueprint of your tables and columns).
* If it sees nested lists/objects, it automatically creates child tables.

  * Example: `items` table becomes `items__nested` for a nested list.
* If new fields appear in the source, dlt evolves the schema automatically (schema evolution).
* If data doesn’t fit the schema, you can apply **contracts** that define how strict to be.

👉 Beginners’ note: Normalization is like dlt saying: *“Okay, I see you have users with addresses and orders. Let me create a clean set of tables for you.”*

---

### 3. Load: Moving Data Into the Destination

Finally, dlt **loads your structured data** into the chosen destination.

```python
pipeline.load()
```

* dlt applies schema migrations if needed.
* Data is written in parallel chunks (“load jobs”) for performance.
* You choose how new data behaves with `write_disposition`:

  * `"append"` → add new rows.
  * `"replace"` → overwrite the entire table.
  * `"merge"` → update existing rows + insert new ones.
* Internal tracking tables are also created (so dlt knows what was loaded and when).

👉 Beginners’ note: Loading is like putting your groceries neatly in the fridge 🍎🥬🥛. Now you can query them whenever you want.

---

## A Simple Example

```python
import dlt

pipeline = dlt.pipeline(pipeline_name="my_pipeline", destination="duckdb")
pipeline.run(
    [
        {"id": 1},
        {"id": 2},
        {"id": 3, "nested": [{"id": 1}, {"id": 2}]},
    ],
    table_name="items",
)
```

What happens?

1. **Extract**: dlt collects the Python list of dicts.
2. **Normalize**: it sees a nested list, so it creates an extra table `items__nested`.
3. **Load**: it writes everything into a DuckDB database — with the schema ready for you.

Result: From plain Python dicts, you now have a **real database with structured tables**.

---

## Other Features Worth Knowing

* ✅ Runs anywhere Python runs (local, notebooks, orchestrators, cloud).
* ✅ Test locally with DuckDB → swap to BigQuery for production.
* ✅ Built-in Streamlit app and Ibis integration for exploration.
* ✅ Automatic schema migrations — no manual SQL needed.
* ✅ Schema contracts to govern how schemas evolve.
* ✅ Monitoring, tracing, and retry policies included.
* ✅ Works with dbt, Arrow, pandas for transformations.

---

## Why This Matters

For beginners, the hardest part of data engineering is usually:

* *How do I keep my data fresh without reloading everything?*
* *What if the schema changes?*
* *How do I avoid duplicates?*
* *How do I keep track of pipeline state?*

With dlt, all of these are handled automatically.
That’s why understanding **Extract → Normalize → Load** is the key step.

👉 Once you grasp this, every pipeline you build will make sense.

---

## Week 5 Takeaway

By the end of this week, you should be able to explain to someone else:

> “A dlt pipeline extracts raw data, normalizes it into structured tables, and loads it into a destination database. It automatically handles schema evolution, state management, incremental syncs, and merging.”

This is the **ETL superpower** that makes modern data engineering possible.

---

## Part of the Series

| Week  | Theme                   | Focus                                |
| ----- | ----------------------- | ------------------------------------ |
| 1     | REST API → DuckDB       | First pipeline with API data         |
| 2     | MySQL → DuckDB          | Load SQL data into DuckDB            |
| 3     | Filesystem → DuckDB     | Work with CSV & local files          |
| 4     | Build Your Own Pipeline | Modular pipelines with GitHub API    |
| **5** | How dlt Works (Theory)  | Extract → Normalize → Load explained |

---

## Join the Journey

Follow [Mahadi Nagassou](https://www.linkedin.com/in/1997mahadi) to continue learning in public.
Together, we’re building a step-by-step foundation for **modern data engineering** 🌍.

---

## License

MIT License — free to learn, remix, and share.

---

🚀 Next week, we’ll go back to building. This time, with a much clearer understanding of the engine powering our pipelines.

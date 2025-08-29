# Week 4: Build Your Own Data Pipeline with dlt

Welcome to **Week 4** of the *Learning in Public with [dlt](https://github.com/dlt-hub/dlt)* journey! This repository serves as an educational resource that guides you through building modern data pipelines using dlt (Data Load Tool), an open-source Python library. Whether you're a beginner or just getting started with data engineering, this repo is designed to teach you step by step how data pipelines work — from extracting data, transforming it, and loading it — using only Python --.

This is a hands-on, beginner-friendly journey. You don't need to be a coding expert. By reading this README and trying the code, you’ll understand what each part does and how everything fits together.

---

## 🧠 What is dlt?

**dlt (Data Load Tool)** is a Python library that makes it easy to build **ELT pipelines** — which stands for:

* **Extract**: Get the data (from APIs, databases, files, etc.)
* **Load**: Store the data (into tools like DuckDB, BigQuery, etc.)
* **Transform**: Clean, enrich, or reshape the data (optional, using Python)

Think of dlt as your assistant that takes care of many technical parts of building a pipeline, such as:

* 🚀 Schema inference: It guesses the structure of your data (columns, types).
* 🔁 Incremental loading: Only fetch new data every time you run it.
* 🧼 Deduplication: Prevents saving the same data twice.
* 🔐 Secure secrets management: Safely handle API keys or passwords.

In short: dlt helps you focus on **what** data you want and **where** to put it — not the plumbing in between.

---

## 🧱 Repository Structure (What's in this repo?)

This repository contains multiple pipeline scripts that teach dlt concepts step by step:

```
week-04_build-pipeline/
├── .dlt/
│   ├── config.toml                 ← Configuration like GitHub repo name
│   └── secrets.toml                ← API tokens and secrets (NEVER share this)
├── pipelines/
│   ├── quick_start_pipeline.py     ← Start here! Learn the basics
│   ├── github_issues.py            ← Load issues from GitHub using append
│   ├── github_issues_incremental.py ← Load GitHub issues incrementally
│   ├── github_issues_merge.py      ← Prevent duplicate issues using merge
│   ├── github_with_source.py       ← Refactor with reusable sources
│   └── github_dynamic_source.py    ← Dynamically load issues by repo name
├── requirements.txt
└── README.md
```

Each script builds on the previous one. You will:

* Start simple (load a Python dictionary)
* Learn to pull real data from GitHub
* Learn how to avoid reloading old data
* Learn how to clean and structure pipelines

---

## 🧠 Key Concepts in dlt

To understand what each script is doing, here are some terms you’ll see:

* `@dlt.resource`: A Python function that fetches or generates data. Think of it like a data tap.
* `@dlt.source`: A group of resources bundled together (like one source per API).
* `dlt.pipeline()`: A pipeline object to define where to store data and how to run it.
* `write_disposition`: This tells dlt **how** to write data. Choose from:

  * `"append"` – add new rows
  * `"replace"` – delete old and add all again
  * `"merge"` – keep existing, add new, and update changed
* `@dlt.incremental`: Enables incremental loading based on fields like `updated_at` or IDs.

---

## 🚀 Learning Modules Explained

### 1. `quick_start_pipeline.py`

Learn by doing: this script loads a simple Python dictionary into DuckDB. This teaches how dlt runs a basic pipeline and shows you where data is saved.

### 2. `github_issues.py`

Now we’re pulling real data from GitHub’s public API. It fetches issues from a repository and appends them to DuckDB. You’ll learn how to connect to an API.

### 3. `github_issues_incremental.py`

Fetching data again and again is wasteful. This script introduces **incremental loading** so that only new or updated issues are added each time you run the pipeline.

### 4. `github_issues_merge.py`

What if GitHub edits an issue? You want to update it, not duplicate it. This script uses **merge** mode to do just that: deduplicate and keep your database clean.

### 5. `github_with_source.py`

This refactors our code using `@dlt.source`. It’s cleaner, modular, and easier to reuse across projects. You’ll learn how to organize your code.

### 6. `github_dynamic_source.py`

We go dynamic! Instead of hardcoding the GitHub repo, this version lets you pass repo names on the fly. Perfect for general-purpose tools.

---

## 🔐 Configuration & Secrets Management

To connect to GitHub or configure your pipeline, dlt uses files in the `.dlt/` directory:

### ✅ `.dlt/secrets.toml`

Store sensitive values here (never upload to GitHub):

```toml
github_token = "ghp_your_personal_access_token"
```

### ⚙ `.dlt/config.toml`

Customize pipeline parameters like which GitHub repo to fetch:

```toml
repo_name = "dlt-hub/dlt"
```

These are safe, standardized files that dlt reads automatically. Do not hardcode secrets in Python scripts!

---

## 🛠 How to Set Up & Run This Project

### 1. Clone the Repo

If you're new to GitHub, this command copies the code to your computer:

```bash
git clone https://github.com/your-username/week-04_build-pipeline.git
cd week-04_build-pipeline
```

### 2. Set Up a Virtual Environment

This creates an isolated Python space for your project:

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
```

### 3. Install Required Python Libraries

```bash
pip install -r requirements.txt
```

### 4. Configure Your `.dlt` Folder

Create `.dlt` folder and the two required files:

```bash
mkdir .dlt
nano .dlt/secrets.toml          # or use any text editor
nano .dlt/config.toml
```

Paste the required values in each file as shown above.

### 5. Run a Pipeline

Try one of the scripts:

```bash
python pipelines/github_issues.py
```

You’ll see logs, schema detection, and a `.dlt` folder created with state and data.

### 6. Visualize Data with Streamlit

Want to explore your loaded data?

```bash
dlt pipeline github_issues show
```

This launches a visual UI where you can inspect your data.

---

## 🎯 Why This Week Matters

This week teaches you real-world data skills:

* Build your own pipelines from scratch
* Optimize data syncs with timestamps or IDs
* Refactor into clean, modular, production-ready code
* Understand data freshness and efficiency
* Learn how to prepare pipelines for scale (e.g. BigQuery, Snowflake)

All using just Python and the magic of dlt ✨

---

## 📚 Part of a Bigger Learning Series

| Week  | Theme                   | Focus                           |
| ----- | ----------------------- | ------------------------------- |
| 1     | REST API → DuckDB       | Consume REST API data           |
| 2     | MySQL → DuckDB          | Load SQL data into DuckDB       |
| 3     | Filesystem → DuckDB     | Load flat files                 |
| **4** | Build Your Own Pipeline | Modular pipelines with dlt      |
| 5     | To Be Announced         | Advanced use cases & deployment |

---

## 🤝 Join the Journey

Follow [Mahadi Nagassou][LinkedIn](https://www.linkedin.com/in/mahadi-nagassou-850a87254/) and connect with a growing community of learners. This repo is part of the movement to build real-world tech skills, especially in Africa 🌍. Everyone is welcome to learn, remix, and share.

Got questions or want to contribute? Open an issue or pull request!

---

## 📝 License

MIT License — learn freely, remix responsibly, and teach others.

---

Let’s build future-proof data pipelines together. One script at a time.

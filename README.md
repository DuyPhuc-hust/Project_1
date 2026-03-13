<a name="readme-top"></a>

<div align="center">

# Meta Spy

Meta Spy is a lightweight **Python-based OSINT tool** designed to collect and analyze **Facebook friendship data**.
</div>

The tool allows users to:

- Log into a Facebook account
- Scrape a user's friend list
- Build a **graph of connections** based on collected friendship data



---

# About The Project

Meta Spy is a research-oriented tool for **social network data collection and analysis**.

The project focuses on a simple workflow:

1. Login to Facebook
2. Scrape friendship data from a target account
3. Generate a network graph representing relationships between collected users

This tool can be useful for **OSINT investigations, social network analysis, and research purposes**.

---

# Features

## Login

Authenticate into a Facebook account using the CLI.

Supports:

- Standard login
- Two-step verification login

---

## Friend List Scraping

Collect friendship data from a specified Facebook account.

Collected information may include:

- Friend IDs
- Profile names
- Public profile information

The data is stored locally for later analysis.

---

## Graph Visualization

Generate a **network graph** showing relationships between collected users based on friendship connections.

This allows users to visualize:

- Social connections
- Network clusters
- Relationship structures

---

# Tech Stack

Backend

- Python
- Typer (CLI framework)
- Selenium (web automation)

Database

- SQLite

Visualization

- Graph generation based on scraped friendship data

---

# Installation

1. Clone git repository
```bash
git clone https://github.com/DuyPhuc-hust/Meta-spy.git
```

2. Create dotenv file and add required data
```bash
cp .env_example .env
```

3. Install all requirements
```bash
pip install -r requirements.txt
```

4. Change directory to metaspy to run commands
```bash
cd metaspy
```

# Login

1. Fill account information in .env file
2. Run 
```bash
python main.py login-2-step
```
OR

```bash
python main.py login
```

# Start tools
1. Run 
```bash
python build_demo.py
```
2. Fill the information you want

# ⚠️Note
Due to recent updates made by Facebook, some parts of this tool may no longer function as expected.

Facebook has changed the structure of elements within their HTML pages to prevent automated data scraping. As a result, certain scraping features in this project — such as collecting friend lists or profile data — may fail or return incomplete results.

This project is maintained primarily for **educational and research purposes**, especially for studying:

- OSINT techniques
- Web scraping challenges
- Social network analysis

Future updates may be required to adapt the scraper to the new page structure.

# References
This project was inspired by and partially based on the following project:

- https://github.com/DEENUU1/meta-spy
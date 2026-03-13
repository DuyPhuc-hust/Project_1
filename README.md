<a name="readme-top"></a>

<div align="center">

# Meta Spy

Meta Spy is a lightweight **Python-based OSINT tool** designed to collect and analyze **Facebook friendship data**.

The tool allows users to:

- Log into a Facebook account
- Scrape a user's friend list
- Build a **graph of connections** based on collected friendship data

</div>

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
git clone https://github.com/DEENUU1/meta-spy.git
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
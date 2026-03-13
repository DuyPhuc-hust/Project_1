<a name="readme-top"></a>

<div align="center">

# Meta Spy

Meta Spy is a lightweight **Python OSINT tool** designed to collect and analyze **Facebook friendship data**.

The tool allows users to:

- Log into a Facebook account
- Scrape a user's friend list
- Build a **graph of connections** based on collected friendship data

</div>

---

# About The Project

Meta Spy is a research-oriented tool used for **social network data collection and analysis**.

It focuses on a simple workflow:

1. Login to Facebook
2. Collect friendship data from a target profile
3. Build a network graph showing connections between collected users

The project can be useful for **OSINT investigations, social network analysis, and research purposes**.

---

# Features

### Login

Authenticate into a Facebook account using the CLI.

Supports:

- Standard login
- Two-step verification login

---

### Friend List Scraping

Collect friendship data from a given Facebook account.

Collected data includes:

- Friend IDs
- Profile names
- Basic public profile information

The collected data is stored locally for later analysis.

---

### Graph Visualization

Build a **network graph** representing relationships between collected users.

The graph allows users to visualize:

- Connections between profiles
- Social clusters
- Network structure

---

# Tech Stack

Backend:

- Python
- Typer (CLI framework)
- Selenium (web automation)

Database:

- SQLite

Visualization:

- Graph generation based on collected friendship data

---

# Installation

### Clone repository

```bash
git clone https://github.com/DEENUU1/meta-spy.git
# Hotspot – Motorbike Theft Web App

## Overview

Hotspot is a platform that helps riders identify motorbike theft hotspots across Victoria.  
It aggregates open crime and transport data into **suburb-level risk scores** with a **safe parking finder**.  
This supports informed parking and travel decisions, reduces theft risk, and strengthens the motorbike community

The project aligns with **UN Sustainable Development Goal 11: Sustainable Cities and Communities**, focusing on making urban areas safer and more resilient

## Project Structure

The repo is split into three main parts:

- **`src/data/`** – data pipeline for generating the SQLite database from raw CSVs
- **`src/api/`** – FastAPI backend serving our API
- **`src/web/`** – Vue 3 frontend showcasing the App

The **Makefile** in the project root provides shortcuts to work with all components.

## Prerequisites

- **Python 3.11+** with [`uv`](https://docs.astral.sh/uv/getting-started/installation/) for the API
- **Node.js 20+** and npm for the web frontend
- **SQLite3** CLI for building the local database

## Common Commands

From the project root:

### Setup & Build

```bash
# Generate the SQLite database from schema + CSVs
make db

# Build the web frontend
make build
```

### Run in Development

```
# Run both API (http://localhost:8000) and Web (http://localhost:5173)
make dev

# Run only the API (dev mode, auto-reloads)
make dev-api

# Run only the Web (dev mode, hot-reloads)
make dev-web
```


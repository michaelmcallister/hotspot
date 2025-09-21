# Hotspot – Motorbike Theft Web App [![CI/CD to App Runner](https://github.com/michaelmcallister/hotspot/actions/workflows/deploy.yaml/badge.svg)](https://github.com/michaelmcallister/hotspot/actions/workflows/deploy.yaml)

## Overview

Hotspot is a platform that helps riders identify motorbike theft hotspots across Victoria.  
It aggregates open crime and transport data into **suburb-level risk scores** with a **safe parking finder**. 
Additional educational and support resources are also linked within the app.
This supports informed parking and travel decisions, reduces theft risk, and strengthens the motorbike community.

The project aligns with **UN Sustainable Development Goal 11: Sustainable Cities and Communities**, focusing on making urban areas safer and more resilient

## Demo
You can try out **Hotspot - Motorbike Theft Web App** here:
[Live Web App](https://pnwuvfcpqp.ap-southeast-2.awsapprunner.com/)

Below is a preview of the app interface:
![Hotspot Screenshot](docs/app-screenshot.png?raw=true)

## Project Structure

The repo is split into three main parts:

- **`src/data/`** – data pipeline for generating the SQLite database from raw CSVs
- **`src/api/`** – FastAPI backend serving our API
- **`src/web/`** – Vue 3 frontend showcasing the App

The **Makefile** in the project root provides shortcuts to work with all components.

## Prerequisites

### For Local Development
- **Python 3.11+** with [`uv`](https://docs.astral.sh/uv/getting-started/installation/) for the API
- **Node.js 20+** and npm for the web frontend
- **SQLite3** CLI for building the local database

### For Docker
- **Docker** installed and running

## Common Commands

From the project root:

### Docker (Quickest way to get started)

```bash
# Build and run the container (serves on http://localhost:8000)
make docker-run

# Stop the container
make docker-stop

# View container logs
make docker-logs

# Access container shell
make docker-shell
```

### Local Development

#### Setup & Build

```bash
# Generate the SQLite database from schema + CSVs
make db

# Build the web frontend
make build
```

#### Run in Development

```bash
# Run both API (http://localhost:8000) and Web (http://localhost:5173)
make dev

# Run only the API (dev mode, auto-reloads)
make dev-api

# Run only the Web (dev mode, hot-reloads)
make dev-web
```


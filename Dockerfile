FROM python:3.13-slim AS api-builder

WORKDIR /app

RUN pip install --no-cache-dir uv

# Copy API source and dependencies
COPY src/api/pyproject.toml ./api/
COPY src/api/uv.lock ./api/
COPY src/api/ ./api/

WORKDIR /app/api
RUN uv sync --frozen --no-dev

FROM node:20-alpine AS web-builder

RUN apk add --no-cache make bash

WORKDIR /app/web

# Copy all web source files including Makefile
COPY src/web/ ./

# Build the frontend using Makefile
RUN make build

# DB build stage
FROM alpine:latest AS db-builder

# Install SQLite and bash
RUN apk add --no-cache sqlite bash make

WORKDIR /app/data

# Copy data generation files
COPY src/data/ ./

# Generate the database using Makefile
RUN make

# Runtime image
FROM python:3.13-slim

# Install uv in the runtime image
RUN pip install --no-cache-dir uv

WORKDIR /app/api

# Create venv in the final image
COPY src/api/pyproject.toml ./
COPY src/api/uv.lock ./
RUN uv sync --frozen --no-dev

ENV PATH="/app/api/.venv/bin:$PATH"
ENV PYTHONPATH=/app/api

COPY src/api/ ./

COPY --from=web-builder /app/web/dist /app/web/dist
COPY --from=db-builder /app/data/hotspot.db /app/data/hotspot.db

EXPOSE 8000

CMD ["/app/api/.venv/bin/python", "main.py", "--static", "/app/web/dist", "--db", "/app/data/hotspot.db"]

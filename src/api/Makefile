SHELL := bash
.ONESHELL:
.DELETE_ON_ERROR:

PYTHON := python
UV := uv
HOST := 0.0.0.0
PORT := 8000

.PHONY: all install run dev clean

all: run

install:
	@echo "Installing dependencies..."
	@$(UV) sync

run: install
	@echo "Starting API backend on $(HOST):$(PORT)..."
	@$(UV) run uvicorn main:app --host $(HOST) --port $(PORT)

dev: install
	@echo "Starting API backend in development mode with auto-reload..."
	@$(UV) run uvicorn main:app --host $(HOST) --port $(PORT) --reload

clean:
	@echo "Cleaning up..."
	@rm -rf __pycache__ .pytest_cache
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
SHELL := bash
.ONESHELL:
.DELETE_ON_ERROR:

.PHONY: all db api web run run-api run-web dev dev-api dev-web clean clean-db clean-api clean-web build

all: db run

db:
	@echo "Generating SQLite database..."
	@$(MAKE) -C src/data

api:
	@echo "Starting API backend..."
	@$(MAKE) -C src/api run

web:
	@echo "Starting web frontend..."
	@$(MAKE) -C src/web run

run: run-api run-web

run-api: db api

run-web: web

dev: db
	@echo "Starting both API and web frontend in development mode..."
	@echo "API will run on http://localhost:8000"
	@echo "Web will run on http://localhost:5173"
	@$(MAKE) -C src/api dev & $(MAKE) -C src/web dev

dev-api: db
	@echo "Starting API backend in development mode..."
	@$(MAKE) -C src/api dev

dev-web:
	@echo "Starting web frontend in development mode..."
	@$(MAKE) -C src/web dev

build: db
	@echo "Building web frontend..."
	@$(MAKE) -C src/web build

clean: clean-db clean-api clean-web

clean-db:
	@echo "Cleaning database..."
	@$(MAKE) -C src/data clean

clean-api:
	@echo "Cleaning API..."
	@$(MAKE) -C src/api clean

clean-web:
	@echo "Cleaning web..."
	@$(MAKE) -C src/web clean

rebuild: clean all
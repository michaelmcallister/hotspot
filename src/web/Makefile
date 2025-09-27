SHELL := bash
.ONESHELL:
.DELETE_ON_ERROR:

NPM := npm
HOST := localhost
PORT := 5173

.PHONY: all install run dev build preview clean format lint format-check lint-check

all: run

install:
	@echo "Installing dependencies..."
	@$(NPM) install

run: install
	@echo "Starting web frontend on http://$(HOST):$(PORT)..."
	@$(NPM) run dev

dev: run

build: install
	@echo "Building production bundle..."
	@$(NPM) run build

preview: build
	@echo "Previewing production build..."
	@$(NPM) run preview

clean:
	@echo "Cleaning up..."
	@rm -rf node_modules dist
	@rm -f package-lock.json

format: install
	@echo "Formatting code with Prettier..."
	@$(NPM) run format

format-check: install
	@echo "Checking code formatting with Prettier..."
	@$(NPM) run format:check

lint: install
	@echo "Linting code with ESLint..."
	@$(NPM) run lint:fix

lint-check: install
	@echo "Checking code with ESLint..."
	@$(NPM) run lint
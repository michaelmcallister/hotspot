SHELL := bash
.ONESHELL:
.DELETE_ON_ERROR:

NPM := npm
HOST := localhost
PORT := 5173

.PHONY: all install run dev build preview clean

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
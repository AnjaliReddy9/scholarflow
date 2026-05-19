.PHONY: help infra-up infra-down api-install api-dev api-test api-lint ingest-install ingest ingest-test web-install web-dev lint pre-commit

ROOT := $(shell pwd)
COMPOSE := docker compose -f infra/docker/docker-compose.yml
VENV ?= .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

RUN_ID ?= local-$(shell date -u +%Y%m%dT%H%M%SZ)

help:
	@echo "Targets: infra-up, ingest-install, ingest, ingest-test, api-install, api-dev, api-test, web-install, web-dev, lint"

$(VENV)/bin/activate:
	python3 -m venv $(VENV)

infra-up:
	$(COMPOSE) up -d

infra-down:
	$(COMPOSE) down

api-install: $(VENV)/bin/activate
	$(PIP) install -U pip
	$(PIP) install -e packages/schemas
	$(PIP) install -e packages/common
	$(PIP) install -e "apps/api[dev]"

api-dev: api-install
	$(VENV)/bin/uvicorn campusiq_api.app:app --reload --host 0.0.0.0 --port 8000

api-test: api-install
	$(VENV)/bin/pytest apps/api/tests -q

api-lint: api-install
	$(VENV)/bin/ruff check apps/api packages/schemas services/retrieval
	$(VENV)/bin/ruff format --check apps/api packages/schemas services/retrieval

ingest-install: api-install
	$(PIP) install -e "services/retrieval[dev]"

ingest: ingest-install
	$(VENV)/bin/campusiq-ingest --raw-dir data/raw --processed-dir data/processed --ingest-run-id $(RUN_ID)

ingest-test: ingest-install
	$(VENV)/bin/pytest services/retrieval/tests -q

web-install:
	cd apps/web && npm ci

web-dev:
	cd apps/web && npm start

lint: api-lint ingest-test

pre-commit:
	pre-commit run --all-files

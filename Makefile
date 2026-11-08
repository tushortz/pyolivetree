.DEFAULT_GOAL := help

.PHONY: help install generate lint format test build docs security run integration deploy-testpypi deploy-pypi

help: ## Show this help
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies with uv
	uv sync --extra dev

generate: ## Regenerate client code from swagger.yml
	uv run python scripts/generate_client.py
	uv run black src/pyolivetree/resources src/pyolivetree/models src/pyolivetree/_operations.py tests/operation_registry.py

lint: ## Run black and ruff checks
	uv run black --check src tests scripts examples
	uv run ruff check src tests scripts examples

format: ## Auto-format code
	uv run black src tests scripts examples
	uv run ruff check --fix src tests scripts examples

test: ## Run lint and unit tests with coverage
	./scripts/run_tests.sh

build: ## Build sdist and wheel
	uv build

docs: ## Build Sphinx HTML documentation
	uv run sphinx-build -W -b html docs docs/_build/html

security: ## Scan dependencies with pysentry-rs
	uvx pysentry-rs .

run: ## Run sync basic example
	uv run python examples/sync_basic.py

integration: ## Run live API integration harness
	uv run python scripts/run_integration.py

deploy-testpypi: build ## Publish to TestPyPI
	uv publish --index testpypi

deploy-pypi: build ## Publish to PyPI
	uv publish

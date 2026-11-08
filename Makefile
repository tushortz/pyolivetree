# Requires uv: https://docs.astral.sh/uv/
.DEFAULT_GOAL := help
.PHONY: help install test coverage lint format docs docs-serve security run build check publish-test publish clean

help: ## Show targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  \033[36m%-13s\033[0m %s\n", $$1, $$2}'

install: ## Create .venv with the package, dev and docs extras
	uv sync --extra dev --extra docs

test: ## Run tests
	uv run pytest -q

coverage: ## Run tests with a coverage report
	uv run pytest -q --cov=pyolivetree --cov-report=term-missing

lint: ## Check style
	uv run ruff check src tests

format: ## Auto-fix style
	uv run ruff check --fix src tests
	uv run ruff format src tests
	uv run black src tests

docs: ## Build HTML docs into docs/_build/html
	uv run sphinx-build -W -b html docs docs/_build/html

docs-serve: docs ## Build docs and serve them on http://localhost:8000
	python3 -m http.server -d docs/_build/html 8000

security: ## Scan dependencies for known vulnerabilities
	uvx pysentry-rs .

run: ## Run the sync example (needs .env)
	uv run python examples/sync_basic.py

build: clean ## Build sdist and wheel into dist/
	uv build

check: build ## Validate dist/ for PyPI
	uv run twine check dist/*

publish-test: check ## Upload to TestPyPI (needs UV_PUBLISH_TOKEN for test.pypi.org)
	uv publish --publish-url https://test.pypi.org/legacy/

publish: check ## Upload to PyPI (needs UV_PUBLISH_TOKEN)
	uv publish

clean: ## Remove build outputs
	rm -rf dist build docs/_build *.egg-info

.PHONY: install lint type-check test docker-test

# Install dependencies using uv
install:
	curl -LsSf https://astral.sh/uv/install.sh | sh
	uv sync --all-extras --dev

# Run Ruff for lightning-fast linting
lint:
	uv run ruff check .

# Run Pyright for static type checking
type-check:
	uv run pyright .

# Run Pytest for unit and analysis tests
test:
	uv run pytest

# Build and run tests inside a Docker container
docker-test:
	docker build -t project-chimera-audit -f Dockerfile .
	docker run --rm project-chimera-audit
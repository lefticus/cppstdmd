# Makefile - Convenient commands for development

.PHONY: help install lint format test coverage clean setup-hooks

# Default target
help:
	@echo "Available targets:"
	@echo "  make install      - Install dependencies (pip install -r requirements.txt)"
	@echo "  make lint         - Run all linters (black, ruff, mypy, pytest)"
	@echo "  make format       - Auto-format code (black, ruff --fix)"
	@echo "  make test         - Run test suite"
	@echo "  make coverage     - Run tests with coverage report"
	@echo "  make setup-hooks  - Install pre-commit hooks"
	@echo "  make clean        - Remove generated files"

# Install dependencies
install:
	./venv/bin/pip install -r requirements.txt

# Run all linters
lint:
	./lint.sh

# Auto-format code
format:
	./format.sh

# Run test suite
test:
	./venv/bin/pytest tests/ -v

# Run tests with coverage
coverage:
	./venv/bin/pytest tests/ --cov=src --cov=generate_diffs --cov=generate_html_site --cov-report=html --cov-report=term

# Install pre-commit hooks
setup-hooks:
	./venv/bin/pre-commit install
	@echo "Pre-commit hooks installed successfully!"
	@echo "Hooks will run automatically on 'git commit'"

# Clean generated files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf htmlcov/ 2>/dev/null || true
	rm -rf .coverage 2>/dev/null || true
	@echo "Cleaned generated files"

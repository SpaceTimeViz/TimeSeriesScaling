SHELL := /bin/bash
EXECUTABLE := poetry run

.PHONY: clean install-dev test run-local-jupyter help

## Clean up temporary files
clean:
	@echo "Cleaning up..."
	@find . -type f -name '*.py[co]' -delete
	@find . -type d -name '__pycache__' -delete
	@rm -rf build/ dist/ .eggs/
	@find . -name '*.egg-info' -exec rm -rf {} +
	@rm -f .coverage
	@rm -rf .pytest_cache

## Install development dependencies
install-dev:
	@echo "Installing development dependencies..."
	@$(SHELL) envs/conda/build_conda_env.sh -c ts-scaler

## Run tests
test:
	@echo "Running tests..."
	@$(EXECUTABLE) pytest --cov=timeseriesscaling

## Start Jupyter server locally
run-local-jupyter:
	@echo "Starting local Jupyter server..."
	@$(SHELL) envs/jupyter/start_jupyter_lab.sh --port 8501

## Display help information
help:
	@echo "Available targets:"
	@echo "  clean                : Clean up temporary files"
	@echo "  install-dev          : Install development dependencies"
	@echo "  test                 : Run tests"
	@echo "  run-local-jupyter    : Start Jupyter server locally"
	@echo "  help                 : Display this help message"


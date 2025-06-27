SHELL=/bin/bash -e

VERSION := $(shell grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
IMAGE_NAME := otp-mcp

.PHONY: help isort black clean venv inspector test

help:
	@echo - make isort       Run isort to sort imports
	@echo - make black       Run black to format code
	@echo - make clean       Clean the project directory
	@echo - make venv        Create a virtual environment and install dependencies
	@echo - make inspector   Starting MCP inspector
	@echo - make test        Run tests with coverage

isort:
	isort --profile black otp_mcp tests

black: isort
	black otp_mcp tests

clean:
	-rm -rf build dist pyvenv.cfg *.egg-info .venv

venv:
	uv venv
	uv pip install -e .
	uv pip install -e ".[dev]"
	uv pip compile pyproject.toml -o requirements.txt

inspector:
	npx @modelcontextprotocol/inspector --config mcp.json --server otp

test:
	uv run pytest -v --cov=otp_mcp --cov-report=term-missing

tag:
	git tag v${VERSION}

image:
	@DOCKER_BUILDKIT=1 docker build \
		 --tag ${IMAGE_NAME} \
		 --tag ${IMAGE_NAME}:latest \
		 --tag ${IMAGE_NAME}:${VERSION} \
		 .


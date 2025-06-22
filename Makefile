SHELL=/bin/bash -e

help:
	@echo - make isort	     Run isort to sort imports
	@echo - make black	 	 Run black to format code
	@echo - make clean	     Clean the project directory
	@echo - make venv	     Create a virtual environment and install dependencies
	@echo - make inspector   Starting MCP inspector

isort:
	isort --profile black otp_mcp

black: isort
	black otp_mcp

clean:
	-rm -rf build dist pyvenv.cfg *.egg-info .venv

venv:
	uv venv
	uv pip install -e .
	uv pip install -e ".[dev]"
	uv pip compile pyproject.toml -o requirements.txt

inspector:
	npx @modelcontextprotocol/inspector --config mcp.json --server otp

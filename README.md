# OTP-MCP-Server

![](https://badge.mcpx.dev?type=server "MCP Server")
[![Build Status](https://github.com/andreax79/otp-mcp/workflows/Tests/badge.svg)](https://github.com/andreax79/otp-mcp/actions)
[![PyPI version](https://badge.fury.io/py/otp-mcp-server.svg)](https://badge.fury.io/py/otp-mcp-server)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

<a href="https://glama.ai/mcp/servers/@andreax79/otp-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@andreax79/otp-mcp/badge" alt="otp-mcp-server MCP server" />
</a>

Model Context Protocol (MCP) server that provides OTP (One-Time Password) generation

A Model Context Protocol (MCP) server built with FastMCP
that provides secure OTP (One-Time Password) generation.
Supports TOTP (Time-based) and HOTP (HMAC-based) algorithms
and multiple transport options including stdio, SSE, and HTTP Stream
for seamless integration with AI assistants and applications.

## Quick Start

### Installation

```bash
# Use uvx for isolated execution
uvx otp-mcp-server

# Or install from PyPI
pip install otp-mcp-server
```

### Basic Usage

```bash
# Run with STDIO (default, for Claude Desktop)
otp-mcp-server

# Run with HTTP Stream transport
otp-mcp-server --http-stream --host 127.0.0.1 --port 8000

# Run with SSE transport
otp-mcp-server --sse --host 127.0.0.1 --port 8000
```

### Using with Claude Desktop

Add to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "otp": {
      "command": "uvx",
      "args": ["otp-mcp-server"]
    }
  }
}
```
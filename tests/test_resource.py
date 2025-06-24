from pathlib import Path

import pytest
from fastmcp import Client

from otp_mcp import resource, server

assert resource

test_dir = Path(__file__).parent
db = test_dir / "test.db"
server.init_token_db(db)


@pytest.mark.asyncio
async def test_ping():
    async with Client(server.mcp) as client:
        # Test connection to the server
        await client.ping()
        # List available operations
        await client.list_tools()
        await client.list_resources()
        await client.list_prompts()


@pytest.mark.asyncio
async def test_get_resource_data_tokens():
    async with Client(server.mcp) as client:
        result = await client.read_resource("data://tokens")
        text = str(result)
        assert "inspired" in text
        assert "petroleum" in text

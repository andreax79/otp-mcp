from pathlib import Path

import pytest
from fastmcp import Client
from fastmcp.exceptions import ToolError

from otp_mcp import server, tool

assert tool

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
async def test_list_otp_tokens():
    async with Client(server.mcp) as client:
        result = await client.call_tool("list_otp_tokens")
        text = str(result)
        assert "inspired" in text
        assert "petroleum" in text


@pytest.mark.asyncio
async def test_get_details():
    async with Client(server.mcp) as client:
        result = await client.call_tool("get_details", {"pattern": "official"})
        text = str(result)
        assert "official" in text
        assert "care" in text
        assert "TOTP" in text

        with pytest.raises(ToolError):
            await client.call_tool("get_details", {"pattern": "notfound"})


@pytest.mark.asyncio
async def test_calculate_otp_codes():
    async with Client(server.mcp) as client:
        result = await client.call_tool("calculate_otp_codes", {"pattern": "at"})
        text = str(result)
        assert "assistance" in text
        assert "atom" in text

        with pytest.raises(ToolError):
            await client.call_tool("calculate_otp_codes", {"pattern": "notfound"})

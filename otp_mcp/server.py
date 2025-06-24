from pathlib import Path

from fastmcp import FastMCP
from freakotp.token import TokenDb

__all__ = [
    "mcp",
    "get_token_db",
    "init_token_db",
]

# Initialize FastMCP server
mcp = FastMCP("otp", mask_error_details=True)

# Token database
_token_db: TokenDb = TokenDb | None  # type: ignore


def get_token_db() -> TokenDb:
    """Get the token database instance."""
    return _token_db


def init_token_db(path: Path | str) -> None:
    """Set the token database instance."""
    global _token_db
    _token_db = TokenDb(path if isinstance(path, Path) else Path(path))

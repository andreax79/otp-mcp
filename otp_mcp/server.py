#
# MIT License
#
# Copyright (c) 2025 Andrea Bonomi <andrea.bonomi@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

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

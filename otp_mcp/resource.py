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

from .common import ALGORITHMS, TOKEN_TYPES
from .server import get_token_db, mcp


@mcp.resource(
    uri="data://tokens",
    mime_type="application/json",
)
def list_tokens() -> list[dict]:
    """Provides OTP tokens as JSON."""
    db = get_token_db()
    result = []
    for token in db.get_tokens():
        item = token.to_dict()
        item["id"] = f"{token.rowid}#"
        # Remove the secret
        if "secret" in item:
            del item["secret"]
        # Remove the counter if the token is not HOTP
        if "counter" in item and str(token.type) != "HOTP":
            del item["counter"]
        result.append(item)
    return result


@mcp.resource(
    uri="data://token_types",
    mime_type="application/json",
)
def list_token_types() -> list[str]:
    """Provides the list of OTP token types."""
    return TOKEN_TYPES


@mcp.resource(
    uri="data://algorithms",
    mime_type="application/json",
)
def list_algorithms() -> list[str]:
    """Provides the list of the supported OTP algorithms."""
    return ALGORITHMS

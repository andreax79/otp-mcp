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

from typing import Literal

from fastmcp.exceptions import ToolError
from freakotp.secret import Secret
from freakotp.token import Token, TokenType
from pydantic import Field

from .common import ALGORITHMS, TOKEN_TYPES
from .server import get_token_db, mcp


def find_tokens(pattern: str) -> list[Token]:
    """
    Find tokens matching the given pattern.
    """
    db = get_token_db()
    if not pattern:
        return db.get_tokens()
    tokens_list = []
    pattern = pattern.lower()
    for token in db.get_tokens():
        tmp = str(token).lower().strip()
        if pattern in tmp or pattern == f"{token.rowid}#":
            tokens_list.append(token)
    return tokens_list


def format_token(token: Token) -> str:
    """
    Format the token details for display.
    """
    result: list[str] = [
        f"Id: {token.rowid}#",
        f"Type: {token.type.name}",
        f"Algorithm: {token.algorithm}",
        f"Issuer: {token.issuer}",
        f"Account: {token.label}",
        f"Digits: {token.digits}",
    ]
    if token.type == TokenType.HOTP:
        result.append(f"Counter: {token.counter}")
    else:
        result.append(f"Period: {token.period} seconds")
    return "\n".join(result)


@mcp.tool()
async def list_otp_tokens() -> str:
    """
    Returns the list of OTP tokens.
    Use this to understand which tokens are available before trying to generate code.
    """
    db = get_token_db()
    tokens_list = db.get_tokens()
    if not tokens_list:
        return "No OTP tokens found."
    return "\n".join([f"{x.rowid}# {x}" for x in tokens_list])


@mcp.tool()
async def get_details(pattern: str) -> str:
    """
    Get the details of all the OTP tokens matching the pattern

    Args:
        pattern: Token pattern (part of the name or token number)
    """
    tokens_list = find_tokens(pattern)
    if not tokens_list:
        raise ToolError("No OTP tokens found.")
    return "\n---\n".join([format_token(x) for x in tokens_list])


@mcp.tool()
async def calculate_otp_codes(pattern: str) -> str:
    """
    Calculate the OTP code for all tokens matching the pattern.

    Args:
        pattern: Token pattern (part of the name or token number)
    """
    codes = []
    tokens = find_tokens(pattern)
    for token in tokens:
        try:
            otp = token.calculate()
            codes.append(f"{token.rowid}# {str(token)} {otp}")
        except Exception:
            raise ToolError(f"Error generating OTP code for token {token.rowid}# {str(token)}")
    if not codes:
        raise ToolError("No OTP tokens found.")
    return "\n".join(codes)


@mcp.tool()
async def add_token(
    secret: str = Field(description="Secret key Base32"),
    issuer: str = Field(description="Issuer of the OTP token"),
    account: str = Field(description="Account for the OTP token"),
    type: Literal[TOKEN_TYPES] = "TOTP",
    algorithm: Literal[ALGORITHMS] = "SHA1",
    counter: int = Field(0, description="Counter value for HOTP tokens"),
    digits: int = Field(6, description="Number of digits in the OTP code"),
    period: int = Field(30, description="Time period for TOTP tokens in seconds"),
) -> str:
    """
    Add a new OTP token.

    Args:
        secret: Base32 encoded secret key
        issuer: Issuer of the OTP token
        account: Accout for the OTP token
        type: Type of the OTP token (TOTP or HOTP) (default is TOTP)
        algorithm: Hashing algorithm to use (SHA1, SHA256, SHA512, MD5) (default is SHA1)
        counter: Counter value for HOTP tokens (default is 0)
        digits: Number of digits in the OTP code (default is 6)
        period: Time period for TOTP tokens in seconds (default is 30)
    """
    try:
        db = get_token_db()
        token = Token(
            uri=None,
            type=TokenType[type] if type else TokenType.TOTP,
            algorithm=algorithm,
            counter=counter,
            digits=digits,
            issuer=issuer,
            issuer_int=None,
            issuer_ext=None,
            label=account,
            period=period,
            secret=Secret.from_base32(secret),
            token_db=db,
        )
        db.insert(token)
        return "Token added successfully."
    except Exception:
        raise ToolError("Error adding OTP token. Please check the provided parameters.")


@mcp.tool()
async def delete_token(pattern: str) -> str:
    """
    Delete an OTP token matching the pattern.

    Args:
        pattern: Token pattern (part of the name or token number)
    """
    db = get_token_db()
    tokens = find_tokens(pattern)
    if not pattern:
        raise ToolError("Pattern cannot be empty.")
    if not tokens:
        raise ToolError("No OTP tokens found.")
    for token in tokens:
        db.delete()
    return f"{len(tokens)} tokens deleted."

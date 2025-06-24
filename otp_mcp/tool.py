from fastmcp.exceptions import ToolError
from freakotp.token import Token

from .server import get_token_db, mcp


def find_tokens(pattern: str) -> list[Token]:
    db = get_token_db()
    # if not pattern:
    #     return db.get_tokens()
    tokens_list = []
    pattern = pattern.lower()
    for token in db.get_tokens():
        tmp = str(token).lower().strip()
        if pattern in tmp or pattern in f"{token.rowid}#":
            tokens_list.append(token)
    return tokens_list


def format_token(token: Token) -> str:
    result: list[str] = []
    result.append(f"{'Number:':<10} {token.rowid}#")
    for key, value in token.to_dict().items():
        if key == "secret":
            continue
        if key == "counter" and str(token.type) != "HOTP":
            continue
        result.append(f"{key.title() + ':':<10} {value}")
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
            codes.append(f"{token.rowid}# {str(token)}: {otp}")
        except Exception:
            raise ToolError(f"Error generating OTP code for token {token.rowid}# {str(token)}")
    if not codes:
        raise ToolError("No OTP tokens found.")
    return "\n".join(codes)

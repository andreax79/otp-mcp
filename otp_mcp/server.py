from fastmcp import FastMCP
from freakotp.token import Token, TokenDb

__all__ = ["mcp"]

# Initialize FastMCP server
mcp = FastMCP("otp")

# Token database
token_db = TokenDb | None


def find_tokens(pattern: str) -> list[Token]:
    tokens_list = []
    pattern = pattern.lower()
    for token in token_db.get_tokens():
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
    tokens_list = token_db.get_tokens()
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
        return "No OTP tokens found."
    return "\n---\n".join([format_token(x) for x in tokens_list])

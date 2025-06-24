from .server import get_token_db, mcp


@mcp.resource(
    uri="data://tokens",
    mime_type="application/json",
)
def get_resource_data_tokens() -> list[dict]:
    """Provides OTP tokens as JSON."""
    db = get_token_db()
    result = []
    for token in db.get_tokens():
        item = token.to_dict()
        if "secret" in item:
            del item["secret"]
        if "counter" in item and str(token.type) != "HOTP":
            del item["counter"]
        result.append(item)
    return result

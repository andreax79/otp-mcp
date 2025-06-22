import argparse
import logging
import sys

from freakotp.cli import DEFAULT_DB
from freakotp.token import TokenDb

from . import server

__all__ = ["main"]

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8000
DEFAULT_PATH = "/mcp"


def parse_args() -> argparse.Namespace:
    "Parse command line arguments"
    parser = argparse.ArgumentParser(
        description="OTP MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # FreakOTP arguments
    parser.add_argument(
        "--db",
        default=DEFAULT_DB,
        help=f"FreakOTP database path: {DEFAULT_DB})",
    )

    # Transport options
    transport_group = parser.add_mutually_exclusive_group()
    transport_group.add_argument("--stdio", action="store_true", help="Use stdio transport (default)")
    transport_group.add_argument("--sse", action="store_true", help="Use SSE transport")
    transport_group.add_argument("--http-stream", action="store_true", help="Use HTTP Stream transport")

    # Network arguments
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help=f"Host to bind to for network transports (default: {DEFAULT_HOST})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Port to bind to for network transports (default: {DEFAULT_PORT})",
    )
    parser.add_argument(
        "--path",
        default=DEFAULT_PATH,
        help=f"Endpoint path (default: {DEFAULT_PATH})",
    )

    # Additional common arguments
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set the logging level",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    # Logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Init FreakOTP
    server.token_db = TokenDb(args.db)

    try:
        if args.http_stream:
            # HTTP Stream Transport
            server.mcp.run(
                transport="streamable-http",
                host=args.host,
                port=args.port,
                path=args.path,
                log_level=args.log_level,
            )

        elif args.sse:
            # Server-Sent Events transport
            server.mcp.run(
                transport="sse",
                host=args.host,
                port=args.port,
                path=args.path,
                log_level=args.log_level,
            )
        else:
            # Default to stdio transport
            server.mcp.run(transport="stdio")

    except KeyboardInterrupt:
        print("\nServer stopped by user")
        return 0
    except Exception as ex:
        print(f"Server error: {ex}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

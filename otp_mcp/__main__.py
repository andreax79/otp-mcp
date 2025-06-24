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

import logging
import sys

import click
from freakotp.cli import DEFAULT_DB

from . import resource, server, tool

__all__ = ["main"]

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8000
DEFAULT_PATH = "/mcp"


@click.command()
@click.option(
    "--db",
    default=DEFAULT_DB,
    show_default=True,
    help="FreakOTP database path",
    type=click.Path(),
    envvar="FREAKOTP_DB",
)
@click.option(
    "--stdio",
    is_flag=True,
    default=False,
    help="Use stdio transport (default)",
)
@click.option("--sse", is_flag=True, default=False, help="Use SSE transport")
@click.option(
    "--http-stream",
    is_flag=True,
    default=False,
    help="Use HTTP Stream transport",
)
@click.option(
    "--host",
    default=DEFAULT_HOST,
    show_default=True,
    help="Host to bind to for network transports",
)
@click.option(
    "--port",
    default=DEFAULT_PORT,
    show_default=True,
    type=int,
    help="Port to bind to for network transports",
)
@click.option(
    "--path",
    default=DEFAULT_PATH,
    show_default=True,
    help="Endpoint path",
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]),
    default="INFO",
    show_default=True,
    help="Set the logging level",
)
def main(
    db,
    stdio,
    sse,
    http_stream,
    host,
    port,
    path,
    log_level,
):
    # Logging
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Initialize the token database
    server.init_token_db(db)

    try:
        if http_stream:
            # HTTP Stream Transport
            server.mcp.run(
                transport="streamable-http",
                host=host,
                port=port,
                path=path,
                log_level=log_level,
            )

        elif sse:
            # Server-Sent Events transport
            server.mcp.run(
                transport="sse",
                host=host,
                port=port,
                path=path,
                log_level=log_level,
            )
        else:
            # Default to stdio transport
            server.mcp.run(transport="stdio")

    except KeyboardInterrupt:
        print("\nServer stopped by user")
        sys.exit(0)
    except Exception as ex:
        print(f"Server error: {ex}", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

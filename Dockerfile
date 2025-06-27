FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS uv

WORKDIR /app
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev --no-editable

ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable

FROM python:3.11-slim-bookworm

WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
ENV OTP_MCP_SERVER_DB="/app/freakotp.db"

RUN adduser mcp && chown mcp:mcp /app

COPY --from=uv --chown=app:app /app/.venv /app/.venv

USER mcp:
EXPOSE 8000

ENTRYPOINT ["otp-mcp-server"]

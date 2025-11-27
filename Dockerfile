FROM python:3.12-slim

# System deps (optional but handy)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install uv (for uvx) and other dependencies
RUN pip install --no-cache-dir uv fastapi uvicorn snowflake-labs-mcp requests pydantic openai

# Copy app code & config
COPY app.py .
COPY auth ./auth
COPY llms ./llms
COPY models ./models
COPY services ./services
COPY entrypoint.sh ./entrypoint.sh

RUN chmod +x /app/entrypoint.sh

ENV SNOWFLAKE_MCP_PORT=9000
ENV SNOWFLAKE_MCP_ENDPOINT=/snowflake-mcp
ENV API_PORT=8000

EXPOSE 8000 9000

ENTRYPOINT ["/app/entrypoint.sh"]
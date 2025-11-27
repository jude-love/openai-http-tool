#!/usr/bin/env bash
set -e

# defaults (can be overridden by env)
: "${SNOWFLAKE_MCP_PORT:=9000}"
: "${SNOWFLAKE_MCP_ENDPOINT:=/snowflake-mcp}"

echo "Starting Snowflake MCP server on port ${SNOWFLAKE_MCP_PORT}${SNOWFLAKE_MCP_ENDPOINT}"...

uvx snowflake-labs-mcp \
  --account "${SNOWFLAKE_ACCOUNT}" \
  --user "${SNOWFLAKE_USER}" \
  --private-key-file /run/keys/snowflake \
  --role "${SNOWFLAKE_ROLE}" \
  --warehouse "${SNOWFLAKE_WAREHOUSE}" \
  --service-config services/tools_config.yaml \
  --transport streamable-http \
  --server-host 127.0.0.1 \
  --port "${SNOWFLAKE_MCP_PORT}" \
  --endpoint "${SNOWFLAKE_MCP_ENDPOINT}" \
  --require-approval always &
MCP_PID=$!

echo "Starting FastAPI on port ${API_PORT:-8000}"...
uvicorn app:app --host 0.0.0.0 --port "${API_PORT:-8000}" &

wait $MCP_PID

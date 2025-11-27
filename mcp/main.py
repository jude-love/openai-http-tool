# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI(title="Rebtel Snowflake MCP Wrapper")


class Info(BaseModel):
    mcp_endpoint: str
    mcp_port: int
    snowflake_account: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/info", response_model=Info)
def info():
    return Info(
        mcp_endpoint=os.getenv("SNOWFLAKE_MCP_ENDPOINT", "/snowflake-mcp"),
        mcp_port=int(os.getenv("SNOWFLAKE_MCP_PORT", "9000")),
        snowflake_account=os.getenv("SNOWFLAKE_ACCOUNT"),
    )

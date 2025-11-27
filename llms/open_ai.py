import os
from openai import OpenAI
from models import AuthedUser
from llms.base import LLM

client = OpenAI()  # uses OPENAI_API_KEY
SNOWFLAKE_MCP_URL = os.environ["SNOWFLAKE_MCP_URL"]


class OpenAILLM(LLM):
    def ask(self, question: str, user: AuthedUser) -> str:
        """
        Use the OpenAI Responses API with the Snowflake MCP server.
        We also pass along user identity context in the instructions
        so GPT can, if you want, shape queries by user.
        """
        response = client.responses.create(
            model="gpt-4o",
            instructions=(
                "You are a data assistant for Snowflake.\n"
                f"The current user is {user.email} (Google sub: {user.google_sub}). "
                "Use the Snowflake MCP tools when you need live data. "
                "Return a concise, user-ready answer."
            ),
            input=question,
            tools=[
                {
                    "type": "mcp",
                    "server_label": "snowflake-mcp",
                    "server_url": SNOWFLAKE_MCP_URL,
                    "require_approval": "never",
                }
            ],
        )

        return response.output_text

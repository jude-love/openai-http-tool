# app.py
import os
from fastapi import FastAPI, Depends
from models import QuestionRequest, AnswerResponse, AuthedUser
from authentication.authenticator import get_current_user
from llms.base import LLM
from llms.open_ai import OpenAILLM

app = FastAPI()

def get_llm() -> LLM:
    llm_provider = os.environ.get("LLM_PROVIDER", "openai").lower()
    if llm_provider == "openai":
        return OpenAILLM()
    # Add other providers here
    else:
        # fallback to default
        return OpenAILLM()

llm = get_llm()


# ---------- HTTP endpoint used by the GPT Action ----------

@app.post("/answer", response_model=AnswerResponse)
async def answer(
    req: QuestionRequest,
    user: AuthedUser = Depends(get_current_user),
):
    """
    This will only succeed if the GPT Action has a valid Google token
    and sends it in the Authorization header. 'user' contains your
    per-user identifier information.
    """
    # Here you can do per-user logic, logging, etc.
    # For example:
    #   - check user.email domain == "rebtel.com"
    #   - map user.google_sub to an internal user_id / Snowflake role
    answer = llm.ask(req.question, user=user)
    return AnswerResponse(answer=answer)

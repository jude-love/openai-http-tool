from typing import Optional
from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str


class AuthedUser(BaseModel):
    google_sub: str         # stable Google user id
    email: str
    name: Optional[str] = None

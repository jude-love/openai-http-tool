from abc import ABC, abstractmethod
from models import AuthedUser


class LLM(ABC):
    @abstractmethod
    def ask(self, question: str, user: AuthedUser) -> str:
        pass

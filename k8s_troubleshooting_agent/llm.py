"""LangChain-compatible LLM provider factory."""

from abc import ABC, abstractmethod


def create_llm(provider: str, model: str):
    """Create a LangChain LLM instance for the given provider and model."""
    provider = provider.lower()
    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=model, temperature=0.0)
    if provider in {"ollama", "local"}:
        from langchain_ollama import ChatOllama

        return ChatOllama(model=model, temperature=0.0)
    if provider in {"anthropic", "claude"}:
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(model=model, temperature=0.0)
    raise ValueError(f"unsupported LLM provider: {provider}")


class BaseLLM(ABC):
    """Abstract base for provider-specific LLM wrappers."""

    @abstractmethod
    def predict(self, prompt: str) -> str:
        """Return a string prediction for the given prompt."""

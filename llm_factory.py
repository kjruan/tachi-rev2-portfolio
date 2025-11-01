"""
LLM Factory - Multi-Provider Language Model Support
Supports: Ollama, OpenRouter, Groq, Claude API, and more
"""

import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment
load_dotenv()


class LLMProvider:
    """Supported LLM providers"""
    OLLAMA = "ollama"
    OPENROUTER = "openrouter"
    GROQ = "groq"
    CLAUDE = "claude"
    OPENAI = "openai"


class LLMFactory:
    """
    Factory for creating LLM instances from multiple providers.
    Handles provider selection, fallbacks, and configuration.
    """

    # Default models per provider
    DEFAULT_MODELS = {
        LLMProvider.OLLAMA: {
            "strategist": "qwen2.5:14b",
            "analyst": "llama3.2:latest",
            "fetcher": "llama3.2:latest",
        },
        LLMProvider.OPENROUTER: {
            "strategist": "meta-llama/llama-3.2-3b-instruct:free",
            "analyst": "meta-llama/llama-3.2-3b-instruct:free",
            "fetcher": "meta-llama/llama-3.2-1b-instruct:free",
        },
        LLMProvider.GROQ: {
            "strategist": "llama-3.3-70b-versatile",
            "analyst": "llama-3.1-70b-versatile",
            "fetcher": "llama-3.1-8b-instant",
        },
        LLMProvider.CLAUDE: {
            "strategist": "claude-sonnet-4-20250514",
            "analyst": "claude-sonnet-4-20250514",
            "fetcher": "claude-3-5-haiku-20241022",
        },
    }

    @staticmethod
    def get_provider() -> str:
        """Get active provider from environment"""
        return os.getenv("LLM_PROVIDER", LLMProvider.OLLAMA).lower()

    @staticmethod
    def get_model_name(role: str) -> str:
        """
        Get model name for a specific role based on provider.

        Args:
            role: Agent role (strategist, analyst, fetcher)
        """
        provider = LLMFactory.get_provider()

        # Check for role-specific override
        env_key = f"{role.upper()}_MODEL"
        if env_model := os.getenv(env_key):
            return env_model

        # Get default for provider
        if provider in LLMFactory.DEFAULT_MODELS:
            return LLMFactory.DEFAULT_MODELS[provider].get(role, "llama3.2:latest")

        return "llama3.2:latest"

    @staticmethod
    def create_llm(role: str = "analyst", temperature: float = 0.7, max_tokens: int = 4096):
        """
        Create an LLM instance for the specified role.

        Args:
            role: Agent role (strategist, analyst, fetcher)
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response

        Returns:
            LangChain LLM instance
        """
        provider = LLMFactory.get_provider()
        model_name = LLMFactory.get_model_name(role)

        try:
            if provider == LLMProvider.OLLAMA:
                return LLMFactory._create_ollama(model_name, temperature, max_tokens)

            elif provider == LLMProvider.OPENROUTER:
                return LLMFactory._create_openrouter(model_name, temperature, max_tokens)

            elif provider == LLMProvider.GROQ:
                return LLMFactory._create_groq(model_name, temperature, max_tokens)

            elif provider == LLMProvider.CLAUDE:
                return LLMFactory._create_claude(model_name, temperature, max_tokens)

            else:
                # Fallback to Ollama
                print(f"Unknown provider '{provider}', falling back to Ollama")
                return LLMFactory._create_ollama("llama3.2:latest", temperature, max_tokens)

        except Exception as e:
            print(f"Error creating LLM with {provider}: {e}")
            print("Attempting fallback to Ollama...")
            return LLMFactory._create_ollama("llama3.2:latest", temperature, max_tokens)

    @staticmethod
    def _create_ollama(model: str, temperature: float, max_tokens: int):
        """Create Ollama LLM instance"""
        from langchain_ollama import OllamaLLM

        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

        return OllamaLLM(
            model=model,
            base_url=base_url,
            temperature=temperature,
            num_predict=max_tokens,
        )

    @staticmethod
    def _create_openrouter(model: str, temperature: float, max_tokens: int):
        """Create OpenRouter LLM instance"""
        from langchain_openai import ChatOpenAI

        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment")

        return ChatOpenAI(
            model=model,
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=temperature,
            max_tokens=max_tokens,
        )

    @staticmethod
    def _create_groq(model: str, temperature: float, max_tokens: int):
        """Create Groq LLM instance"""
        from langchain_groq import ChatGroq

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment")

        return ChatGroq(
            model=model,
            groq_api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    @staticmethod
    def _create_claude(model: str, temperature: float, max_tokens: int):
        """Create Claude LLM instance (original implementation)"""
        from langchain_anthropic import ChatAnthropic

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")

        return ChatAnthropic(
            model=model,
            anthropic_api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    @staticmethod
    def verify_provider() -> bool:
        """
        Verify that the configured provider is available and working.

        Returns:
            bool: True if provider is working, False otherwise
        """
        provider = LLMFactory.get_provider()

        try:
            if provider == LLMProvider.OLLAMA:
                import requests
                base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
                response = requests.get(f"{base_url}/api/tags", timeout=5)
                return response.status_code == 200

            elif provider == LLMProvider.OPENROUTER:
                api_key = os.getenv("OPENROUTER_API_KEY")
                return api_key is not None and len(api_key) > 0

            elif provider == LLMProvider.GROQ:
                api_key = os.getenv("GROQ_API_KEY")
                return api_key is not None and len(api_key) > 0

            elif provider == LLMProvider.CLAUDE:
                api_key = os.getenv("ANTHROPIC_API_KEY")
                return api_key is not None and len(api_key) > 0

            return False

        except Exception as e:
            print(f"Provider verification failed: {e}")
            return False

    @staticmethod
    def list_available_providers() -> Dict[str, bool]:
        """
        Check which providers are currently available.

        Returns:
            Dictionary mapping provider names to availability status
        """
        import requests

        available = {}

        # Check Ollama
        try:
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            response = requests.get(f"{base_url}/api/tags", timeout=2)
            available[LLMProvider.OLLAMA] = response.status_code == 200
        except:
            available[LLMProvider.OLLAMA] = False

        # Check OpenRouter
        available[LLMProvider.OPENROUTER] = bool(os.getenv("OPENROUTER_API_KEY"))

        # Check Groq
        available[LLMProvider.GROQ] = bool(os.getenv("GROQ_API_KEY"))

        # Check Claude
        available[LLMProvider.CLAUDE] = bool(os.getenv("ANTHROPIC_API_KEY"))

        return available


# Convenience functions for backward compatibility
def get_strategist_model():
    """Get strategist LLM (high reasoning)"""
    return LLMFactory.create_llm("strategist", temperature=0.7, max_tokens=4096)


def get_analyst_model():
    """Get analyst LLM (balanced)"""
    return LLMFactory.create_llm("analyst", temperature=0.5, max_tokens=4096)


def get_fetcher_model():
    """Get fetcher LLM (fast, simple)"""
    return LLMFactory.create_llm("fetcher", temperature=0.3, max_tokens=2048)


# Export
__all__ = [
    "LLMFactory",
    "LLMProvider",
    "get_strategist_model",
    "get_analyst_model",
    "get_fetcher_model",
]

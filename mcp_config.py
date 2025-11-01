"""
MCP (Model Context Protocol) Configuration
Manages MCP servers and tool integrations
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()


class MCPConfig:
    """Configuration for MCP servers and tools"""

    # MCP Server configurations
    MCP_SERVERS = {
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
            "description": "Local filesystem access",
            "enabled": False,  # Disabled by default for security
        },
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {
                "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN", "")
            },
            "description": "GitHub repository access",
            "enabled": bool(os.getenv("GITHUB_TOKEN")),
        },
        "brave-search": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-brave-search"],
            "env": {
                "BRAVE_API_KEY": os.getenv("BRAVE_API_KEY", "")
            },
            "description": "Web search via Brave",
            "enabled": bool(os.getenv("BRAVE_API_KEY")),
        },
    }

    @staticmethod
    def get_enabled_servers() -> Dict[str, dict]:
        """Get list of enabled MCP servers"""
        return {
            name: config
            for name, config in MCPConfig.MCP_SERVERS.items()
            if config.get("enabled", False)
        }

    @staticmethod
    def is_mcp_enabled() -> bool:
        """Check if any MCP servers are enabled"""
        return len(MCPConfig.get_enabled_servers()) > 0

    @staticmethod
    def list_available_servers() -> List[str]:
        """List all available MCP servers"""
        return list(MCPConfig.MCP_SERVERS.keys())

    @staticmethod
    def enable_server(server_name: str) -> bool:
        """
        Enable an MCP server.

        Args:
            server_name: Name of the server to enable

        Returns:
            bool: True if successful, False otherwise
        """
        if server_name in MCPConfig.MCP_SERVERS:
            MCPConfig.MCP_SERVERS[server_name]["enabled"] = True
            return True
        return False

    @staticmethod
    def disable_server(server_name: str) -> bool:
        """
        Disable an MCP server.

        Args:
            server_name: Name of the server to disable

        Returns:
            bool: True if successful, False otherwise
        """
        if server_name in MCPConfig.MCP_SERVERS:
            MCPConfig.MCP_SERVERS[server_name]["enabled"] = False
            return True
        return False


# Tool integration configurations
class ToolConfig:
    """Configuration for tool integrations"""

    # Native tools (our custom implementations)
    NATIVE_TOOLS_ENABLED = True

    # MCP tools (from MCP servers)
    MCP_TOOLS_ENABLED = MCPConfig.is_mcp_enabled()

    # Tool prioritization (native first, then MCP)
    TOOL_PRIORITY = ["native", "mcp"]

    @staticmethod
    def should_use_native_tools() -> bool:
        """Check if native tools should be used"""
        return ToolConfig.NATIVE_TOOLS_ENABLED

    @staticmethod
    def should_use_mcp_tools() -> bool:
        """Check if MCP tools should be used"""
        return ToolConfig.MCP_TOOLS_ENABLED and MCPConfig.is_mcp_enabled()


# Provider-specific settings
class ProviderSettings:
    """Settings for different LLM providers"""

    # Ollama settings
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))

    # OpenRouter settings
    OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
    OPENROUTER_SITE_URL = os.getenv("OPENROUTER_SITE_URL", "https://github.com")
    OPENROUTER_APP_NAME = os.getenv("OPENROUTER_APP_NAME", "rev2-portfolio")

    # Groq settings
    GROQ_API_BASE = "https://api.groq.com/openai/v1"

    # Rate limiting (requests per minute)
    RATE_LIMITS = {
        "ollama": None,  # No limit for local
        "openrouter": 20,  # Conservative default
        "groq": 30,  # Groq free tier
        "claude": 5,  # Claude free tier
    }

    @staticmethod
    def get_rate_limit(provider: str) -> Optional[int]:
        """Get rate limit for provider"""
        return ProviderSettings.RATE_LIMITS.get(provider.lower())


# Analysis configuration
class AnalysisConfig:
    """Configuration for portfolio analysis behavior"""

    # Timeout for analysis tasks (seconds)
    ANALYSIS_TIMEOUT = int(os.getenv("ANALYSIS_TIMEOUT", "300"))

    # Number of retries on failure
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

    # Enable verbose output
    VERBOSE = os.getenv("VERBOSE", "false").lower() == "true"

    # Enable agent memory
    ENABLE_MEMORY = os.getenv("ENABLE_MEMORY", "true").lower() == "true"

    # Maximum concurrent analyses
    MAX_CONCURRENT = int(os.getenv("MAX_CONCURRENT", "3"))


def print_configuration():
    """Print current configuration"""
    print("=" * 60)
    print("Rev2 Configuration")
    print("=" * 60)

    # LLM Provider
    from llm_factory import LLMFactory
    provider = LLMFactory.get_provider()
    print(f"\nLLM Provider: {provider}")

    # Available providers
    available = LLMFactory.list_available_providers()
    print("\nAvailable Providers:")
    for prov, avail in available.items():
        status = "✓" if avail else "✗"
        print(f"  {status} {prov}")

    # MCP Servers
    print("\nMCP Servers:")
    if MCPConfig.is_mcp_enabled():
        enabled = MCPConfig.get_enabled_servers()
        for name, config in enabled.items():
            print(f"  ✓ {name}: {config['description']}")
    else:
        print("  (none enabled)")

    # Tools
    print("\nTool Configuration:")
    print(f"  Native Tools: {'Enabled' if ToolConfig.NATIVE_TOOLS_ENABLED else 'Disabled'}")
    print(f"  MCP Tools: {'Enabled' if ToolConfig.MCP_TOOLS_ENABLED else 'Disabled'}")

    # Analysis
    print("\nAnalysis Settings:")
    print(f"  Timeout: {AnalysisConfig.ANALYSIS_TIMEOUT}s")
    print(f"  Max Retries: {AnalysisConfig.MAX_RETRIES}")
    print(f"  Verbose: {AnalysisConfig.VERBOSE}")
    print(f"  Memory: {AnalysisConfig.ENABLE_MEMORY}")

    print("=" * 60)


if __name__ == "__main__":
    print_configuration()

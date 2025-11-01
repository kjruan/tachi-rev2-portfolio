# Rev2 Quick Start Guide

Get rev2 running in 5 minutes!

## Prerequisites

- Python 3.9+ installed
- **One of the following** (choose based on your preference):
  - **Ollama** (local/free - recommended for getting started)
  - **OpenRouter** API key (free tier available)
  - **Groq** API key (free tier available)
  - **Claude** API key (paid, requires credits)

See [MCP_SETUP.md](MCP_SETUP.md) for detailed comparison and setup instructions.

## Setup (5 Steps)

### 1. Navigate to rev2
```bash
cd rev2
```

### 2. Activate Virtual Environment
```bash
# Already created for you!
source .venv/bin/activate    # macOS/Linux
# or
.venv\Scripts\activate       # Windows
```

### 3. Configure Your LLM Provider

**Option A: Ollama (Recommended - Local/Free)**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh  # Linux
# or: brew install ollama  # macOS

# Start Ollama
ollama serve

# Copy template
cp .env.example .env
# LLM_PROVIDER=ollama is already set by default!
```

**Option B: OpenRouter (Free Tier)**
```bash
# Get free API key from: https://openrouter.ai/keys

# Copy and edit .env
cp .env.example .env

# Edit .env and set:
# LLM_PROVIDER=openrouter
# OPENROUTER_API_KEY=your_key_here
```

**Option C: Groq (Free Tier)**
```bash
# Get free API key from: https://console.groq.com/keys

# Copy and edit .env
cp .env.example .env

# Edit .env and set:
# LLM_PROVIDER=groq
# GROQ_API_KEY=your_key_here
```

**Option D: Claude (Paid)**
```bash
# Get API key from: https://console.anthropic.com/
# Note: Requires $5 minimum credit

# Copy and edit .env
cp .env.example .env

# Edit .env and set:
# LLM_PROVIDER=claude
# ANTHROPIC_API_KEY=sk-ant-api03-...
```

See [MCP_SETUP.md](MCP_SETUP.md) for detailed comparison and configuration.

### 4. Verify Setup
```bash
python config.py
```
You should see:
- `Active Provider: ollama` (or your chosen provider)
- `Configuration verified successfully`

### 5. Run!
```bash
python main.py
```

## Usage

### CLI - Interactive Analysis

```bash
python main.py
```

**Try the examples:**
- Option 3: Analyze Tech Portfolio (AAPL, MSFT, GOOGL, NVDA)
- Option 4: Analyze Single Stock (AAPL)

**Or create your own:**
- Option 1: Enter your portfolio
- Option 2: Analyze any stock

### API Server - For Integration

```bash
python api/server.py
```

API runs on `http://localhost:8001`
- View docs: http://localhost:8001/docs
- Test health: http://localhost:8001/health

**Quick API Test:**
```bash
curl http://localhost:8001/health
```

## First Analysis (Example)

```bash
$ python main.py
# Select: 3 (Example: Tech Portfolio)
# Wait 2-5 minutes for analysis
# Get comprehensive AI report!
```

## Troubleshooting

### Provider Not Configured
```bash
# Check which provider is active
python config.py

# For Ollama: Make sure it's running
ollama serve

# For API providers: Check your .env file
cat .env | grep API_KEY
```

### "ModuleNotFoundError"
```bash
# Activate virtual environment
source .venv/bin/activate

# Verify
which python  # Should show .venv path
```

### "Command not found: python"
```bash
# Try python3 instead
python3 main.py
```

### Ollama Issues
```bash
# Model not found - pull it:
ollama pull qwen2.5:14b      # Strategist
ollama pull llama3.2:latest  # Analyst/Fetcher

# Connection refused - start server:
ollama serve
```

### API Key Invalid
- **OpenRouter**: Get key from https://openrouter.ai/keys
- **Groq**: Get key from https://console.groq.com/keys
- **Claude**: Get key from https://console.anthropic.com/ (requires credits)
- Make sure to copy the full key
- Check no extra spaces in .env file

## What's Next?

- **Provider Setup**: See [MCP_SETUP.md](MCP_SETUP.md) for detailed provider comparison and configuration
- **Full Documentation**: See [README.md](README.md) for complete details
- **Architecture**: Learn about the 5 AI agents and how they work together
- **API Integration**: Connect with tachi-cli main app via REST API
- **Customization**: Add your own tools, agents, and strategies

## Quick Reference

```bash
# Activate environment
source .venv/bin/activate

# Run CLI
python main.py

# Run API server
python api/server.py

# Check config
python config.py

# Run tests
python test_imports.py
```

---

**Need Help?** Check the full [README.md](README.md) or the [context/REV2_PORTFOLIO_GUIDE.md](../context/REV2_PORTFOLIO_GUIDE.md)

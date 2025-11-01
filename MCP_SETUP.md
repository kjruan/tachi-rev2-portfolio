# MCP & Multi-Provider Setup Guide

Rev2 now supports multiple LLM providers, giving you flexibility to use local models (free) or cloud APIs. This guide helps you choose and configure your preferred provider.

## Provider Comparison

| Provider | Cost | Speed | Quality | Setup Difficulty |
|----------|------|-------|---------|------------------|
| **Ollama** | Free | Medium | Good | Easy (local install) |
| **OpenRouter** | Free tier | Fast | Good | Easy (API key) |
| **Groq** | Free tier | Very Fast | Excellent | Easy (API key) |
| **Claude** | Paid ($) | Fast | Excellent | Easy (API key, requires credits) |

## Quick Setup

### Option 1: Ollama (Recommended for Development)

**Pros:** Free, private, no API keys needed
**Cons:** Requires local installation, uses system resources

1. **Install Ollama:**
   ```bash
   # macOS
   brew install ollama

   # Linux
   curl -fsSL https://ollama.ai/install.sh | sh

   # Windows
   # Download from https://ollama.ai/download
   ```

2. **Start Ollama:**
   ```bash
   ollama serve
   ```

3. **Pull models (automatic on first use, or pre-download):**
   ```bash
   ollama pull qwen2.5:14b      # Strategist (7GB)
   ollama pull llama3.2:latest  # Analyst/Fetcher (2GB)
   ```

4. **Configure rev2:**
   ```bash
   cd rev2
   cp .env.example .env
   # LLM_PROVIDER=ollama is already set by default
   ```

5. **Test:**
   ```bash
   python config.py
   # Should show: "Active Provider: ollama"
   ```

### Option 2: OpenRouter (Free Tier)

**Pros:** Free tier available, no local installation, fast
**Cons:** Requires API key, rate limits

1. **Get API key:**
   - Visit https://openrouter.ai/keys
   - Sign up (free)
   - Create API key

2. **Configure rev2:**
   ```bash
   cd rev2
   cp .env.example .env
   # Edit .env:
   ```

   Set these values:
   ```bash
   LLM_PROVIDER=openrouter
   OPENROUTER_API_KEY=your_key_here
   ```

3. **Test:**
   ```bash
   python config.py
   ```

### Option 3: Groq (Free Tier)

**Pros:** Very fast, generous free tier, excellent quality
**Cons:** Requires API key, rate limits (30/min)

1. **Get API key:**
   - Visit https://console.groq.com/keys
   - Sign up (free)
   - Create API key

2. **Configure rev2:**
   ```bash
   cd rev2
   cp .env.example .env
   # Edit .env:
   ```

   Set these values:
   ```bash
   LLM_PROVIDER=groq
   GROQ_API_KEY=your_key_here
   ```

3. **Test:**
   ```bash
   python config.py
   ```

### Option 4: Claude (Paid)

**Pros:** Highest quality, best reasoning
**Cons:** Requires paid credits ($5 minimum)

1. **Get API key:**
   - Visit https://console.anthropic.com/
   - Add credits (minimum $5)
   - Create API key

2. **Configure rev2:**
   ```bash
   cd rev2
   cp .env.example .env
   # Edit .env:
   ```

   Set these values:
   ```bash
   LLM_PROVIDER=claude
   ANTHROPIC_API_KEY=sk-ant-api03-...
   ```

3. **Test:**
   ```bash
   python config.py
   ```

## Model Configuration

Each provider uses different models optimized for each agent role:

### Default Models by Provider

**Ollama:**
- Strategist: `qwen2.5:14b` (best reasoning)
- Analyst: `llama3.2:latest` (balanced)
- Fetcher: `llama3.2:latest` (fast)

**OpenRouter (free tier):**
- Strategist: `meta-llama/llama-3.2-3b-instruct:free`
- Analyst: `meta-llama/llama-3.2-3b-instruct:free`
- Fetcher: `meta-llama/llama-3.2-1b-instruct:free`

**Groq:**
- Strategist: `llama-3.3-70b-versatile` (best)
- Analyst: `llama-3.1-70b-versatile` (strong)
- Fetcher: `llama-3.1-8b-instant` (fast)

**Claude:**
- Strategist: `claude-sonnet-4-20250514` (best reasoning)
- Analyst: `claude-sonnet-4-20250514` (strong)
- Fetcher: `claude-3-5-haiku-20241022` (fast & cheap)

### Override Default Models

You can override any model in `.env`:

```bash
# Example: Use different Ollama models
STRATEGIST_MODEL=llama3.2:latest
ANALYST_MODEL=mistral:latest
FETCHER_MODEL=phi3:latest
```

## MCP (Model Context Protocol) Integration

MCP servers provide additional capabilities like file access, GitHub integration, and web search.

### Available MCP Servers

1. **Filesystem** - Local file access (disabled by default for security)
2. **GitHub** - Repository access (requires token)
3. **Brave Search** - Web search (requires API key)

### Enabling MCP Servers

MCP servers are optional and require additional configuration:

#### GitHub Integration
```bash
# In .env:
GITHUB_TOKEN=ghp_your_token_here
```

#### Brave Search
```bash
# In .env:
BRAVE_API_KEY=your_brave_key_here
```

MCP tools are automatically available when configured and will be used by agents when needed.

## Performance Tips

### Ollama Performance

1. **GPU Acceleration:** Ollama automatically uses GPU if available
   - Check: `ollama ps` shows GPU memory usage

2. **Model Size:** Balance quality vs speed
   - Large models (13B+): Better quality, slower
   - Small models (3B-7B): Faster, good quality

3. **Concurrent Requests:** Ollama handles one request at a time locally

### API Provider Performance

1. **Rate Limits:**
   - Ollama: No limits (local)
   - OpenRouter: ~20/min (free tier)
   - Groq: 30/min (free tier)
   - Claude: 5/min (free tier)

2. **Caching:** Rev2 automatically handles rate limiting

## Switching Providers

You can switch providers anytime by changing `.env`:

```bash
# Switch from Ollama to Groq
LLM_PROVIDER=groq
GROQ_API_KEY=your_key_here
```

No code changes needed!

## Troubleshooting

### Ollama Issues

**"Connection refused"**
```bash
# Make sure Ollama is running:
ollama serve
```

**"Model not found"**
```bash
# Pull the model:
ollama pull qwen2.5:14b
```

**Slow performance**
- Use smaller models: `llama3.2:latest` instead of larger models
- Check GPU usage: `ollama ps`

### API Provider Issues

**"API key invalid"**
- Check key is correct in `.env`
- Make sure no extra spaces
- For Claude: ensure you have credits

**"Rate limit exceeded"**
- Wait a minute and retry
- Consider upgrading to paid tier
- Switch to Ollama for unlimited local usage

**"Provider not available"**
```bash
# Check configuration:
python mcp_config.py

# Verify provider setup:
python config.py
```

## Advanced Configuration

### Custom Provider Settings

Edit `rev2/llm_factory.py` to add custom providers or modify existing ones.

### Rate Limiting

Adjust rate limits in `rev2/mcp_config.py`:

```python
RATE_LIMITS = {
    "ollama": None,  # No limit
    "openrouter": 20,
    "groq": 30,
    "claude": 5,
}
```

### Analysis Behavior

In `.env`:

```bash
ANALYSIS_TIMEOUT=300      # Seconds per analysis
MAX_RETRIES=3            # Retry on failure
MAX_CONCURRENT=3         # Parallel analyses
VERBOSE=true            # Detailed output
```

## Cost Considerations

### Free Options
- **Ollama:** Completely free, uses your hardware
- **OpenRouter:** Free tier with rate limits
- **Groq:** Free tier, 30 req/min

### Paid Options
- **Claude:** ~$3-15 per million tokens depending on model
  - Haiku: ~$0.25-1.25 per million tokens
  - Sonnet: ~$3-15 per million tokens

### Estimate Usage
A typical portfolio analysis:
- ~10,000-50,000 tokens total
- Claude cost: ~$0.03-0.75 per analysis
- Free tiers: Usually sufficient for personal use

## Recommended Setups

### For Development
```bash
LLM_PROVIDER=ollama
# Free, unlimited, private
```

### For Production (Budget)
```bash
LLM_PROVIDER=groq
GROQ_API_KEY=your_key
# Fast, free tier, good quality
```

### For Production (Best Quality)
```bash
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=your_key
# Best quality, reasonable cost
```

## Next Steps

1. Choose your provider
2. Follow the setup steps above
3. Test: `python config.py`
4. Run: `python main.py`
5. See [QUICKSTART.md](QUICKSTART.md) for usage guide

## Support

- Ollama Docs: https://ollama.ai/docs
- OpenRouter Docs: https://openrouter.ai/docs
- Groq Docs: https://console.groq.com/docs
- Claude Docs: https://docs.anthropic.com
- Rev2 README: [README.md](README.md)

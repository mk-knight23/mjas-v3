# MJAS v3.0 - Mikazi Job Application Swarm

An intelligent, agent-based system for automating job applications across multiple job portals.

## Overview

MJAS (Mikazi Job Application Swarm) is a Python-based automation framework that uses Playwright for browser automation and a multi-agent architecture to intelligently apply to jobs across various platforms.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -e ".[dev]"
   playwright install
   ```

2. **Configure credentials:**
   ```bash
   cp config/credentials.env.example config/credentials.env
   # Edit config/credentials.env with your settings
   ```

3. **Run the application:**
   ```bash
   mjas
   ```

## Project Structure

```
.
├── src/mjas/           # Main source code
│   ├── core/           # Core framework components
│   ├── portals/        # Job portal implementations
│   ├── discovery/      # Job discovery agents
│   ├── agents/         # Application agents
│   └── utils/          # Utilities
├── tests/              # Test suite
│   ├── unit/           # Unit tests
│   └── integration/    # Integration tests
├── config/             # Configuration files
├── data/               # Data storage
├── logs/               # Log files
└── scripts/            # Utility scripts
```

## Development

- Python 3.11+ required
- Uses `pyproject.toml` for modern Python packaging
- Code formatting with Black (line length: 100)
- Linting with Ruff
- Type checking with MyPy (strict mode)
- Testing with pytest

## Full Plan

See the complete upgrade plan at:
`~/.claude/plans/mjas-v3-upgrade-2026-02-19.md`

## License

MIT

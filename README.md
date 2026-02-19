# MJAS v3.0 - Mikazi Job Application Swarm

An intelligent, agent-based system for automating job applications across multiple job portals using real browser automation.

## Overview

MJAS (Mikazi Job Application Swarm) v3.0 is a Python-based automation framework that uses:
- **Playwright** for real browser automation
- **Multi-agent swarm architecture** for parallel job processing
- **Fernet encryption** for secure credential storage
- **SQLite database** for job tracking and state management
- **13 job portals** organized in 3 tiers for maximum coverage

## Quick Start

### 1. Installation

```bash
# Run automated installer
./scripts/install.sh

# Or manually:
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
playwright install chromium
```

### 2. Credential Setup

```bash
# Interactive wizard (recommended)
python scripts/setup_credentials.py

# Or manual:
cp config/credentials.env.example config/credentials.env
# Edit with your credentials
```

### 3. Encrypt Credentials

```bash
python -m mjas setup
```

### 4. Start Applying

```bash
# List all available portals
python -m mjas list-portals

# Run with Tier 1 portals (LinkedIn, Indeed, Wellfound, Naukri)
python -m mjas run --visible --tier 1

# Run continuously every 2 hours
python -m mjas run --continuous --tier 1

# View statistics
python -m mjas stats
```

## Available Portals

| Tier | Portals | Description |
|------|---------|-------------|
| **Tier 1** | LinkedIn, Indeed, Wellfound, Naukri | Major platforms with highest volume |
| **Tier 2** | Glassdoor, ZipRecruiter, Dice | Secondary major platforms |
| **Tier 3** | Otta, RemoteOK, WeWorkRemotely, Hired, SimplyHired, CareerBuilder | Specialized/curated platforms |

**Features:**
- 🔐 = Requires login
- 🌐 = No login required
- [Tech] = AI/Tech focused portal

## Architecture

```
MJAS v3.0 Swarm Architecture:

┌─────────────────────────────────────────────────────────┐
│              SwarmOrchestrator                          │
│  (Coordinates workers, manages global rate limits)      │
└──────────┬──────────────────────────────────────────────┘
           │
    ┌──────┴──────────────────────────────────┐
    │                                          │
    ▼                                          ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ LinkedIn │  │ Indeed   │  │ Wellfound│  │ Naukri   │
│ Worker   │  │ Worker   │  │ Worker   │  │ Worker   │
│ (50/day) │  │ (40/day) │  │ (30/day) │  │ (35/day) │
└──────────┘  └──────────┘  └──────────┘  └──────────┘
      │            │            │            │
      └────────────┴────────────┴────────────┘
                         │
                    ┌────┴────┐
                    │ SQLite  │
                    │ Database│
                    └─────────┘
```

## Daily Limits

| Portal | Max/Day | Delay Range | Login Required |
|--------|---------|-------------|----------------|
| LinkedIn | 50 | 45-90s | Yes |
| Indeed | 40 | 30-60s | Yes |
| Wellfound | 30 | 60-120s | Yes |
| Naukri | 35 | 45-90s | Yes |
| Glassdoor | 25 | 35-70s | Yes |
| ZipRecruiter | 30 | 30-60s | Yes |
| Dice | 25 | 40-80s | Yes |
| Otta | 20 | 60-120s | Yes |
| RemoteOK | 50 | 20-40s | **No** |
| We Work Remotely | 30 | 30-60s | **No** |
| Hired | 15 | 90-180s | Yes |
| SimplyHired | 40 | 25-50s | **No** |
| CareerBuilder | 25 | 35-70s | Yes |
| **Total Potential** | **400+** | - | - |

## CLI Reference

```
python -m mjas [command] [options]

Commands:
  setup          Initialize and encrypt credentials
  run            Run full cycle (research + apply)
  stats          Show statistics
  list-portals   List available job portals

Run Options:
  --portals [name ...]  Specific portals to use
  --tier [1|2|3]        Portal tier to use
  --visible             Show browser window
  --continuous          Run continuously
  --interval MINUTES    Minutes between cycles (default: 120)
  --target NUMBER       Daily application target (default: 200)
  -v, --verbose         Enable verbose logging
```

## Security

- **Encrypted Credentials**: Fernet/AES-128 encryption
- **Separate Key Storage**: Encryption key stored separately from encrypted data
- **File Permissions**: Credential files have user-only access (600)
- **No Credential Logging**: Database contains only job metadata
- **Screenshots**: Saved to `screenshots/` for visual debugging
- **Real Browser**: All automation through Playwright (not HTTP requests)

## Project Structure

```
.
├── src/mjas/              # Main source code
│   ├── core/              # Core framework (vault, database, swarm, worker)
│   ├── portals/           # Job portal implementations (13 portals)
│   ├── discovery/         # MCP-powered portal discovery
│   └── __main__.py        # CLI entry point
├── tests/                 # Test suite
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
├── config/                # Configuration files
│   ├── credentials.env    # Credentials (gitignored)
│   └── *.key              # Encryption keys (gitignored)
├── data/                  # SQLite database
├── logs/                  # Log files
├── screenshots/           # Debug screenshots
└── scripts/               # Utility scripts
    ├── install.sh         # Installation script
    └── setup_credentials.py  # Credential wizard
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `LINKEDIN_EMAIL` / `LINKEDIN_PASSWORD` | LinkedIn credentials |
| `INDEED_EMAIL` / `INDEED_PASSWORD` | Indeed credentials |
| `WELLFOUND_EMAIL` / `WELLFOUND_PASSWORD` | Wellfound credentials |
| `NAUKRI_EMAIL` / `NAUKRI_PASSWORD` | Naukri credentials |
| `GLASSDOOR_EMAIL` / `GLASSDOOR_PASSWORD` | Glassdoor credentials |
| `ZIPRECRUITER_EMAIL` / `ZIPRECRUITER_PASSWORD` | ZipRecruiter credentials |
| `DICE_EMAIL` / `DICE_PASSWORD` | Dice credentials |
| `GMAIL_EMAIL` / `GMAIL_PASSWORD` | For verification codes |
| `GEMINI_API_KEY` | For job matching (optional) |

## Troubleshooting

### CAPTCHA Detected
System will pause the affected portal and save a screenshot. Manually solve the CAPTCHA, then the system will resume on next cycle.

### Login Failures
```bash
# Re-run setup to re-encrypt credentials
python -m mjas setup
```

### Rate Limited
System automatically backs off with exponential delay. Check stats:
```bash
python -m mjas stats
```

### Playwright Browser Not Found
```bash
playwright install chromium
```

### Database Locked
```bash
# Kill any hanging processes
pkill -f "python -m mjas"
# Remove lock file if exists
rm data/mjas.db-journal
```

## Development

- Python 3.11+ required
- Uses `pyproject.toml` for modern Python packaging
- Code formatting with Black (line length: 100)
- Linting with Ruff
- Type checking with MyPy (strict mode)
- Testing with pytest

## Testing

```bash
# Run all tests
pytest

# Run integration tests only
pytest tests/integration/

# Run with coverage
pytest --cov=mjas --cov-report=html
```

## Full Implementation Plan

See the complete upgrade plan at:
`~/.claude/plans/mjas-v3-upgrade-2026-02-19.md`

## License

MIT

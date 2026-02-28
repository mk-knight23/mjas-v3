# MJAS v3.0 - Mikazi Job Application Swarm

An intelligent, agent-based system for automating job applications across multiple job portals using real browser automation.

## Overview

MJAS (Mikazi Job Application Swarm) v3.0 is a Python-based automation framework that uses:
- **Playwright** for real browser automation
- **Multi-agent swarm architecture** for parallel job processing
- **Browser sessions** for authentication (Google Sign-In)
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

### 2. Setup Browser Sessions (One-Time)

```bash
source .venv/bin/activate
python -m mjas setup-sessions --visible
```

This opens browsers for each portal. Click "Sign in with Google" and login with:
**kazimusharraf1234@gmail.com**

### 3. Run

```bash
# List all available portals
python -m mjas list-portals

# Run with Tier 1 portals (LinkedIn, Indeed, Wellfound, Naukri)
python -m mjas run --tier 1

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

Browser Sessions (data/sessions/):
├── linkedin_session.json
├── indeed_session.json
├── wellfound_session.json
└── naukri_session.json
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
  setup-sessions Setup browser sessions with Google Sign-In (one-time)
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

- **Browser Sessions**: Stored in `data/sessions/` as JSON
- **Session Content**: Cookies and local storage (not passwords)
- **File Permissions**: Session files have user-only access (600)
- **No Password Storage**: No credentials stored in code or config
- **Google Sign-In**: Secure OAuth 2.0 authentication
- **Screenshots**: Saved to `screenshots/` for visual debugging
- **Real Browser**: All automation through Playwright (not HTTP requests)

## Project Structure

```
.
├── src/mjas/              # Main source code
│   ├── core/              # Core framework (database, swarm, worker, sessions)
│   ├── portals/           # Job portal implementations (13 portals)
│   ├── discovery/         # MCP-powered portal discovery
│   └── __main__.py        # CLI entry point
├── tests/                 # Test suite
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
├── config/                # Configuration files
├── data/                  # SQLite database + browser sessions
│   ├── sessions/          # Browser session files (gitignored)
│   └── mjas.db            # Job tracking database
├── logs/                  # Log files
├── screenshots/           # Debug screenshots
└── scripts/               # Utility scripts
    └── install.sh         # Installation script
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | For AI-powered job matching (optional) |
| `HEADLESS` | Run browsers in headless mode (default: false) |

## Troubleshooting

### CAPTCHA Detected
System will pause the affected portal and save a screenshot. Manually solve the CAPTCHA, then the system will resume on next cycle.

### Session Expired
```bash
# Re-run session setup to refresh authentication
python -m mjas setup-sessions --visible
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


## 🎯 Problem Solved

This repository provides a streamlined approach to modern development needs, enabling developers to build robust applications with minimal complexity and maximum efficiency.

## ✨ Features

- **Core Functionality:** Primary features and capabilities
- **Production Ready:** Built for real-world deployment scenarios
- **Optimized Performance:** Efficient resource utilization
- **Developer Experience:** Clear documentation and intuitive API

## 🏗️ Architecture

```
```

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/mk-knight23/mjas-v3
cd mjas-v3

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🌐 Deployment

### Live URLs

| Platform | URL |
|----------|-----|
| Vercel | [Deployed Link] |
| GitHub Pages | [Deployed Link] |


## 📄 License

MIT License - see LICENSE file for details

---

Built with ❤️ by mk-knight23
# 🤖 Mikazi Musharraf — Autonomous Job Application Agent System
> **Platform**: Antigravity (or AutoGPT / Relevance AI / AgentGPT)
> **Mode**: 24/7 Autonomous Operation
> **Goal**: Apply to 50-100 jobs per day across all major job portals

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────┐
│               MASTER ORCHESTRATOR                     │
│         (Coordinates all 5 agents)                    │
└──────────┬───────────────────────────────────────────┘
           │
    ┌──────┴──────────────────────────────────┐
    │                                          │
    ▼                                          ▼
┌───────────────┐                    ┌────────────────────┐
│  AGENT 1      │                    │  AGENT 2           │
│  Research     │────scrapes────────▶│  Job Application   │
│  Agent        │    job listings    │  Agent             │
└───────────────┘                    └────────────────────┘
                                              │
              ┌───────────────────────────────┤
              ▼                               ▼
    ┌─────────────────┐           ┌────────────────────┐
    │  AGENT 3        │           │  AGENT 4           │
    │  LinkedIn       │           │  Profile Manager   │
    │  Agent          │           │  Agent             │
    └─────────────────┘           └────────────────────┘
                                              │
                                    ┌─────────▼──────────┐
                                    │  AGENT 5           │
                                    │  Tracker &         │
                                    │  Follow-up Agent   │
                                    └────────────────────┘
```

---

## 👤 Candidate Profile (Fill Before Running)

```yaml
CANDIDATE:
  full_name: "Mikazi Musharraf"
  email: "[YOUR_EMAIL]"
  phone: "[YOUR_PHONE]"
  location: "[YOUR_CITY, COUNTRY]"
  linkedin_url: "[YOUR_LINKEDIN_URL]"
  portfolio: "[YOUR_PORTFOLIO_URL_IF_ANY]"
  github: "[YOUR_GITHUB_IF_ANY]"

RESUME:
  file_path: "./resume/mikazi_musharraf_resume.pdf"
  summary: "[PASTE 2-LINE SUMMARY FROM YOUR RESUME]"

JOB_PREFERENCES:
  titles:
    - "[Job Title 1, e.g. Software Engineer]"
    - "[Job Title 2, e.g. Backend Developer]"
    - "[Job Title 3]"
  locations:
    - "[City 1]"
    - "Remote"
    - "[City 2]"
  salary_min: "[MINIMUM SALARY]"
  salary_max: "[MAXIMUM SALARY]"
  job_types:
    - "Full-time"
    - "Contract"
  experience_level:
    - "Mid-level"
    - "Senior"
  industries:
    - "[Industry 1]"
    - "[Industry 2]"
  exclude_companies:
    - "[Company to avoid 1]"
  keywords:
    - "[Skill 1]"
    - "[Skill 2]"
    - "[Skill 3]"
```

---

## 🎯 Target Job Portals

| Portal | Agent Assigned | Apply Method |
|--------|---------------|--------------|
| LinkedIn | Agent 3 | Easy Apply + Manual |
| Indeed | Agent 2 | Quick Apply |
| Glassdoor | Agent 2 | Direct Apply |
| Naukri.com | Agent 2 | Quick Apply |
| Monster | Agent 2 | Direct Apply |
| Dice | Agent 2 | Easy Apply |
| ZipRecruiter | Agent 2 | One-Click Apply |
| AngelList / Wellfound | Agent 2 | Direct Apply |
| Greenhouse | Agent 2 | Form Fill |
| Lever | Agent 2 | Form Fill |
| Workday | Agent 2 | Form Fill |
| We Work Remotely | Agent 2 | Direct Apply |
| Remote.co | Agent 2 | Direct Apply |
| Hired | Agent 1+2 | Profile Apply |

---

## 📋 Agent Responsibilities Summary

| Agent | Name | Primary Job | Runs Every |
|-------|------|-------------|-----------|
| Agent 1 | Research Agent | Scrape & filter job listings | 2 hours |
| Agent 2 | Application Agent | Fill forms & submit applications | Continuous |
| Agent 3 | LinkedIn Agent | LinkedIn Easy Apply + connections | 30 min |
| Agent 4 | Profile Manager | Keep resume/profiles updated | Daily |
| Agent 5 | Tracker Agent | Log results, follow-ups, analytics | Hourly |

---

## 🔐 Credentials Vault (Store Securely)

```yaml
CREDENTIALS:
  linkedin:
    email: "[LINKEDIN_EMAIL]"
    password: "[LINKEDIN_PASSWORD]"
  indeed:
    email: "[INDEED_EMAIL]"
    password: "[INDEED_PASSWORD]"
  glassdoor:
    email: "[GLASSDOOR_EMAIL]"
    password: "[GLASSDOOR_PASSWORD]"
  naukri:
    email: "[NAUKRI_EMAIL]"
    password: "[NAUKRI_PASSWORD]"
  # Add more as needed
```

> ⚠️ Store credentials using your platform's secret manager, NEVER in plain text files.

---

## 🔁 Master Workflow Loop

```
EVERY 2 HOURS:
  1. Agent 1 → Scrape new jobs from all portals
  2. Agent 1 → Filter by preferences → Pass to Agent 2 queue
  3. Agent 2 → Apply to jobs in queue (batch of 20-30)
  4. Agent 3 → Run LinkedIn Easy Apply in parallel
  5. Agent 5 → Log all applications to tracker sheet
  
EVERY 24 HOURS:
  1. Agent 4 → Refresh profiles on all portals
  2. Agent 4 → Upload latest resume version
  3. Agent 5 → Send daily summary report
  4. Agent 5 → Trigger follow-up emails for 7-day old applications
```

---

## 🛑 Safety Rules (Apply to ALL Agents)

```
RULE 1: Never apply to the same job twice (check tracker first)
RULE 2: Max 100 applications per day across all platforms
RULE 3: Never fabricate or alter resume content
RULE 4: Always use Mikazi's actual credentials, never create fake profiles
RULE 5: Respect platform rate limits — add 3-10s delay between actions
RULE 6: If CAPTCHA detected → pause and notify user via email
RULE 7: Log every action with timestamp in tracker
RULE 8: If login fails → retry 3x then flag for human review
```

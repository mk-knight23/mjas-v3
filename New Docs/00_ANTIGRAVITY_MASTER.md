# ⚡ ANTIGRAVITY MASTER GUIDE — MUSHARRAF KAZI (MIKAZI)
# How Antigravity Actually Works + Full Implementation Plan

---

## 🧠 HOW ANTIGRAVITY'S BROWSER AGENT WORKS

Antigravity (like other modern agent platforms) has a **Live Browser Tool**.
Here is exactly what it can do:

```
✅ Open any URL in a real browser
✅ Click buttons, links, icons
✅ Type text into input fields
✅ Select dropdowns
✅ Check/uncheck checkboxes
✅ Upload files (resume, profile photo)
✅ Scroll up/down on pages
✅ Handle popups and modals
✅ Fill multi-step forms (paginated forms)
✅ Read page content (scrape visible text)
✅ Take screenshots at any point
✅ Handle redirects automatically
✅ Wait for page loads
✅ Handle basic CAPTCHAs (with human-in-loop mode)
✅ Log into websites with credentials
✅ Sign UP to new websites (create accounts)
✅ Navigate tabs
✅ Read success/error messages
```

---

## 🔑 THE KEY CONCEPT: HOW TO GIVE ANTIGRAVITY A TASK

When you create an agent in Antigravity, you write a **PROMPT** that tells it:
1. What website to go to
2. What to do there (login / signup / fill form / apply)
3. What data to use (from your profile)
4. What to do after

**The agent reads your prompt + has browser access = it does the task like a human.**

---

## 👤 YOUR IDENTITY DATA (Pre-filled — Copy Directly)

```yaml
MIKAZI_PROFILE:
  # Personal
  full_name: "Musharraf Kazi"
  public_name: "Mikazi Musharraf"
  first_name: "Musharraf"
  last_name: "Kazi"
  headline: "AI Engineer | Agentic AI Systems | Multi-LLM Orchestration | SaaS Builder"
  
  # Contact (FILL THESE IN)
  email: "[YOUR_EMAIL]"
  phone: "[YOUR_PHONE]"
  city: "[YOUR_CITY]"
  state: "[YOUR_STATE]"
  country: "India"
  zip: "[YOUR_ZIP]"
  
  # Professional Links
  linkedin: "[YOUR_LINKEDIN_URL]"
  github: "[YOUR_GITHUB_URL]"
  portfolio: "[YOUR_PORTFOLIO_URL]"
  
  # Job Search
  target_roles:
    - "AI Engineer"
    - "Generative AI Engineer"
    - "Agentic AI Engineer"
    - "LLM Systems Engineer"
    - "Python Backend Engineer"
    - "Applied AI Engineer"
  
  # Skills (for form fields)
  primary_skills: "Python, LangChain, LangGraph, FastAPI, OpenAI API, RAG Systems, Multi-Agent Architecture, Next.js, Supabase"
  
  # Experience
  total_years_experience: "[X]"
  current_designation: "AI Engineer & Indie Builder"
  
  # Work Preferences  
  work_type: "Remote"
  preferred_locations: "Remote, India"
  open_to_relocate: "No"
  notice_period: "Immediate"
  
  # Salary
  expected_salary_inr: "[X LPA]"
  expected_salary_usd: "[X per year]"
  
  # Education
  degree: "[YOUR DEGREE]"
  specialization: "[YOUR FIELD]"
  university: "[YOUR UNIVERSITY]"
  graduation_year: "[YEAR]"
  
  # Work Authorization
  authorized_india: "Yes"
  need_sponsorship: "No"
  
  # Professional Summary (Use in forms)
  summary: |
    AI Engineer and Indie Builder specializing in Agentic AI Systems, 
    Multi-LLM orchestration, and production-grade AI SaaS development. 
    Builder of the VIBE ecosystem — an AI-native developer platform. 
    Expert in LangGraph, LangChain, OpenAI Agents SDK, RAG systems, 
    FastAPI, and Next.js. Focused on building autonomous AI systems 
    that work at scale.

  # Resume
  resume_file: "musharraf_kazi_ai_engineer_resume.pdf"
```

---

## 🏗️ SYSTEM ARCHITECTURE IN ANTIGRAVITY

```
Antigravity Workspace: "Mikazi Job Agents"
│
├── 🔑 Secrets Vault
│   ├── All platform credentials
│   └── API keys
│
├── 📁 Files
│   ├── musharraf_kazi_ai_engineer_resume.pdf
│   └── CANDIDATE_MASTER_PROFILE.md (this file)
│
├── 🤖 Agents
│   ├── Agent 1: ResearchBot (finds jobs)
│   ├── Agent 2: ApplyBot (applies to jobs)
│   ├── Agent 3: LinkedInBot (LinkedIn specialist)
│   ├── Agent 4: ProfileBot (keeps profiles fresh)
│   └── Agent 5: TrackerBot (tracks everything)
│
└── ⚙️ Workflows
    ├── Pipeline: Research → Apply (every 2hrs)
    ├── Daily: Profile refresh (2 AM)
    └── Daily: Reports (9 AM)
```

---

## 🚦 QUICK START: 4 STEPS TO GO LIVE

```
STEP 1: Create workspace in Antigravity
        Name: "Mikazi Job Application System"

STEP 2: Upload files
        - This .md file
        - Your resume PDF
        - All other .md agent files

STEP 3: Store credentials in Secrets Vault
        - All platform logins

STEP 4: Create each agent (paste prompts from ANTIGRAVITY_SETUP.md)
        - Create Agent 1 first, test it
        - Then add others one by one

STEP 5: Connect workflows and activate
```

---

## 📋 JOB PORTALS SIGN-UP PRIORITY LIST

Do these sign-ups ONCE (manually or via Agent 4):

```
TIER 1 — Do First (Highest AI Job Volume):
□ LinkedIn (linkedin.com)
□ Wellfound / AngelList (wellfound.com) — Best for AI startups
□ Otta (otta.com) — Curated tech jobs
□ Indeed (indeed.com)
□ Glassdoor (glassdoor.com)

TIER 2 — Do Second:
□ Naukri (naukri.com) — India market
□ Instahyre (instahyre.com) — India AI/tech
□ Cutshort (cutshort.io) — India AI/startup
□ Hirect (hirect.in) — India startup direct hiring
□ Dice (dice.com) — Global tech

TIER 3 — Specialized AI Job Boards:
□ AIJobBoard (aijobboard.ai)
□ AI Jobs (aijobs.net)
□ ML Jobs (mljobs.dev)
□ RemoteAI (remoteai.io)
□ Levels.fyi — For comp data
```

---

## 🔐 CREDENTIAL STRATEGY

For each platform, use this structure in Antigravity Secrets:

```
linkedin_email = your.email@gmail.com
linkedin_password = [password]

wellfound_email = your.email@gmail.com
wellfound_password = [password]

indeed_email = your.email@gmail.com
indeed_password = [password]

[etc for each platform]
```

**Tip**: Use the same email across all platforms for easier tracking.
**Tip**: Use a dedicated job-search email (e.g. mikazi.jobs@gmail.com) so all responses go to one place.

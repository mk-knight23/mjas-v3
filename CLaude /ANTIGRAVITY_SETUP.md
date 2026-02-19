# ⚡ ANTIGRAVITY SETUP GUIDE
# How to Deploy All 5 Agents on Antigravity (or AutoGPT / Relevance AI)

---

## 🚀 STEP 1: Initial Setup

### A. Upload Files
Upload all these files to your Antigravity workspace:
```
📁 mikazi_job_agents/
├── MASTER_AGENT_SYSTEM.md       ← Read this first
├── AGENT_1_RESEARCH.md
├── AGENT_2_APPLICATION.md
├── AGENT_3_LINKEDIN.md
├── AGENT_4_PROFILE.md
├── AGENT_5_TRACKER.md
├── resume/
│   └── mikazi_musharraf_resume.pdf   ← ADD YOUR RESUME HERE
└── templates/
    └── cover_letter_template.txt     ← ADD YOUR COVER LETTER
```

### B. Set Environment Variables / Secrets
```
MIKAZI_EMAIL = "[your email]"
MIKAZI_PHONE = "[your phone]"
LINKEDIN_EMAIL = "[linkedin email]"
LINKEDIN_PASSWORD = "[linkedin password]"
INDEED_EMAIL = "[indeed email]"
INDEED_PASSWORD = "[indeed password]"
GLASSDOOR_EMAIL = "[glassdoor email]"
GLASSDOOR_PASSWORD = "[glassdoor password]"
NAUKRI_EMAIL = "[naukri email]"
NAUKRI_PASSWORD = "[naukri password]"
OPENAI_API_KEY = "[your openai key for cover letters]"
NOTIFICATION_EMAIL = "[email to receive daily reports]"
```

---

## 🤖 STEP 2: Create Each Agent in Antigravity

### MASTER PROMPT FOR ANTIGRAVITY UI:

Paste this when creating each agent:

---

#### AGENT 1 PROMPT (Copy-paste into Antigravity):
```
You are ResearchBot-Mikazi, a job research agent working 24/7 for Mikazi Musharraf.

Your job:
1. Log into job portals (LinkedIn, Indeed, Glassdoor, Naukri, Monster, Dice, ZipRecruiter)
2. Search for jobs matching: [JOB_TITLES] in [LOCATIONS]
3. Scrape job listings from the last 24 hours
4. Score each job (0-100) based on relevance to Mikazi's profile
5. Filter out duplicates and low-scoring jobs
6. Save qualified jobs to job_queue.json with status = "queued"
7. Run every 2 hours automatically

Credentials are in the secrets vault.
Resume and profile data are in MASTER_AGENT_SYSTEM.md.
Full detailed instructions are in AGENT_1_RESEARCH.md.

START NOW. Log in to LinkedIn first. Search for jobs posted in the last 24 hours.
```

---

#### AGENT 2 PROMPT:
```
You are ApplyBot-Mikazi, a job application agent working 24/7 for Mikazi Musharraf.

Your job:
1. Check job_queue.json every 15 minutes for new jobs with status = "queued"
2. Apply to each job using the appropriate method (Easy Apply, Quick Apply, or Full Form)
3. Fill all form fields using Mikazi's profile data (in MASTER_AGENT_SYSTEM.md)
4. Generate custom cover letters for each application using AI
5. Submit the application and take a screenshot of confirmation
6. Update job_queue.json status to "applied"
7. Log every application to the master tracker

Credentials, profile data, and resume file path are in MASTER_AGENT_SYSTEM.md.
Full instructions are in AGENT_2_APPLICATION.md.

RULES: Max 100 applications/day. 30-60 second delays between applications. Never fabricate info.

START: Check the queue now and begin applying.
```

---

#### AGENT 3 PROMPT:
```
You are LinkedInBot-Mikazi, a LinkedIn specialist agent working 24/7 for Mikazi Musharraf.

Your job every 30 minutes:
1. Log into LinkedIn
2. Search for jobs with "Easy Apply" filter active
3. Apply to all matching jobs using Easy Apply
4. Send 10-15 strategic connection requests to recruiters daily
5. Reply to any recruiter messages within 2 hours
6. Keep "Open to Work" status active
7. Refresh profile daily

LinkedIn credentials are in secrets vault.
Full detailed instructions in AGENT_3_LINKEDIN.md.
Profile data in MASTER_AGENT_SYSTEM.md.

SAFETY: Max 40 Easy Apply per day. 2-3 minute delays. Human-like behavior.

START: Log into LinkedIn and begin the Easy Apply workflow.
```

---

#### AGENT 4 PROMPT:
```
You are ProfileBot-Mikazi, a profile manager running daily at 2 AM.

Your job:
1. Log into every job portal: Indeed, Glassdoor, Naukri, Monster, Dice, ZipRecruiter, Wellfound
2. For each portal:
   - Upload the latest resume PDF
   - Set "Open to Work" / "Actively Looking" status to ON
   - Update job preferences and salary expectations
   - Refresh/re-upload profile to appear at top of recruiter searches
   - Ensure 100% profile completion
3. Generate daily profile health report
4. Email report to Mikazi

Credentials in secrets vault. Profile data in MASTER_AGENT_SYSTEM.md.
Full instructions in AGENT_4_PROFILE.md.

START: Log into Indeed first and begin profile refresh.
```

---

#### AGENT 5 PROMPT:
```
You are TrackerBot-Mikazi, a tracking and analytics agent running every hour.

Your job:
1. Every hour: Read new applications from queue and log to master tracker spreadsheet
2. Every 6 hours: Check application statuses on each portal for updates
3. Daily (Day 7 after apply): Send follow-up emails to employers
4. Daily 9 AM: Generate and email a full analytics report to Mikazi
5. Instantly: When interview is scheduled, research company and send prep guide

Track everything in Google Sheets (or Airtable). Never miss a follow-up.
Follow-up email templates are in AGENT_5_TRACKER.md.
Full instructions in AGENT_5_TRACKER.md.

START: Check master tracker now. Identify any applications needing follow-up.
```

---

## ⚙️ STEP 3: Workflow Connections (Antigravity Workflow Builder)

```
WORKFLOW: Main Job Application Pipeline

TRIGGER: Every 2 hours (CRON: 0 */2 * * *)

STEP 1: Agent 1 (Research) runs
  → Output: job_queue.json updated

STEP 2: Agent 2 (Application) reads queue
  → Processes next batch of 10 jobs

STEP 3: Agent 3 (LinkedIn) runs in PARALLEL with Agent 2
  → Does its own LinkedIn Easy Apply batch

STEP 4: Agent 5 (Tracker) logs all new applications
  → Updates master spreadsheet

---

WORKFLOW: Daily Maintenance

TRIGGER: Every day at 2:00 AM

STEP 1: Agent 4 (Profile) runs
  → Refreshes all portals

STEP 2: Agent 5 generates daily report
  → Sends email to Mikazi

---

WORKFLOW: Follow-Up Email

TRIGGER: Every day at 10:00 AM

STEP 1: Agent 5 checks tracker
  → Finds applications that are exactly 7 days old
  → Sends follow-up emails
```

---

## 📋 STEP 4: Rules to Set in Antigravity

```
GLOBAL RULES (Apply to ALL agents):

RULE 1: "Before applying to any job, check the master tracker to ensure 
         we haven't already applied. If job_url exists in tracker, SKIP."

RULE 2: "Never exceed 100 total applications per day across all agents combined."

RULE 3: "Always add a random delay of 30-90 seconds between applications 
         to mimic human behavior and avoid bot detection."

RULE 4: "If CAPTCHA is encountered on any website, STOP applying on that 
         platform, log the event, and send an email alert to Mikazi."

RULE 5: "Never modify Mikazi's resume content. Only use information that 
         exists in his profile. Do not fabricate experience or skills."

RULE 6: "All login credentials must be retrieved from the secrets vault. 
         Never store credentials in plain text."

RULE 7: "Take a screenshot of every successful application confirmation page 
         and save it to ./screenshots/ folder."

RULE 8: "If login fails after 3 attempts, skip that portal and send alert."
```

---

## 📊 STEP 5: Dashboard Setup

Create a Google Sheet named "Mikazi Job Tracker" with these tabs:

```
Tab 1: APPLICATIONS (main tracker table)
Tab 2: DAILY STATS (auto-filled by Agent 5)
Tab 3: PORTAL PERFORMANCE (charts)
Tab 4: INTERVIEW PIPELINE
Tab 5: OFFERS
```

Share the Google Sheet with the agent's service account email.

---

## ✅ Launch Checklist

```
□ Resume PDF uploaded to ./resume/ folder
□ All credentials stored in secrets vault
□ Master profile data filled in MASTER_AGENT_SYSTEM.md
□ Google Sheet created and shared
□ All 5 agents created in Antigravity
□ Workflows connected (Research → Application → LinkedIn → Tracker)
□ Cron schedules set for each workflow
□ Test run completed (1 agent, 1 job) — verify application submitted
□ Daily report email configured
□ Emergency stop button configured (to pause all agents)
```

---

## 🛑 EMERGENCY STOP

To stop all agents immediately:
1. In Antigravity: Go to Workflows → Disable all active workflows
2. Or set global variable: `AGENTS_ACTIVE = false`
3. All agents check this flag at the start of each run

---

## 📞 Support & Adjustments

**To add a new job portal:**
→ Edit AGENT_1_RESEARCH.md: Add portal to search list
→ Edit AGENT_2_APPLICATION.md: Add apply workflow for that portal
→ Edit AGENT_4_PROFILE.md: Add profile refresh for that portal

**To change job preferences:**
→ Edit MASTER_AGENT_SYSTEM.md: Update JOB_PREFERENCES section
→ All agents read from this central config

**To pause a specific agent:**
→ Disable that agent's workflow in Antigravity panel
→ Other agents continue running independently
```

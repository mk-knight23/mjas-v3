# 🚀 QUICK START — DO THIS RIGHT NOW
# Step-by-step: From zero to live agents in Antigravity

---

## ⏱️ ESTIMATED TIME: 45 Minutes to Go Live

---

## PHASE 1: SETUP (15 minutes)

### Step 1: Create Your Antigravity Workspace
```
1. Go to: app.antigravity.ai (or your Antigravity URL)
2. Click "New Workspace"
3. Name: "Mikazi Job Application System"
4. Save
```

### Step 2: Upload Your Files
```
In Antigravity → Files section:
□ Upload: musharraf_kazi_ai_engineer_resume.pdf  ← YOUR RESUME
□ Upload: 00_ANTIGRAVITY_MASTER.md (this system)
□ Upload: CANDIDATE_MASTER_PROFILE.md (your profile file)

Name your resume EXACTLY: musharraf_kazi_ai_engineer_resume.pdf
(All agents reference this exact filename)
```

### Step 3: Store Your Credentials
```
In Antigravity → Secrets Vault:

ADD THESE SECRETS:
Key: linkedin_email        Value: [your linkedin email]
Key: linkedin_password     Value: [your linkedin password]
Key: indeed_email          Value: [your indeed email]  
Key: indeed_password       Value: [your indeed password]
Key: naukri_email          Value: [your naukri email]
Key: naukri_password       Value: [your naukri password]
Key: wellfound_email       Value: [your wellfound email]
Key: wellfound_password    Value: [your wellfound password]
Key: candidate_email       Value: [your personal email for notifications]
Key: candidate_phone       Value: [your phone number]
Key: candidate_city        Value: [your city]
Key: candidate_salary      Value: [your expected salary]
Key: candidate_experience  Value: [years of experience]
Key: candidate_linkedin    Value: [your full linkedin profile URL]
Key: candidate_github      Value: [your github URL]
```

---

## PHASE 2: CREATE ACCOUNTS MANUALLY (20 minutes)
*(Do this once — agents will maintain after)*

### Create these accounts YOURSELF first:

```
□ LinkedIn: linkedin.com/signup
  - Name: Musharraf Kazi
  - Headline: "AI Engineer | Agentic AI Systems | Multi-LLM Orchestration"
  - Upload resume, set Open to Work ✓

□ Wellfound: wellfound.com  
  - Sign up as Candidate
  - Set "Actively Looking" ✓
  - Add skills: Python, LangChain, LangGraph, FastAPI, RAG

□ Indeed: indeed.com
  - Create account
  - Upload resume ✓
  - Set "Resume is searchable" ✓

□ Naukri: naukri.com
  - Create account
  - Complete 100% profile
  - Upload resume ✓
  - Set "Show to recruiters" ✓

□ Instahyre: instahyre.com
  - Create account
  - Set active status ✓

Store ALL credentials in secrets vault after creating each account.
```

---

## PHASE 3: CREATE AGENTS (10 minutes)

### Create Agent 1 — Research Bot
```
In Antigravity:
1. Click "New Agent"
2. Name: "ResearchBot-Mikazi"
3. Description: "Finds AI Engineer jobs every 2 hours"
4. Tools to enable:
   ✅ Web Browser
   ✅ File Read
   ✅ Memory/Storage
5. System Prompt: [PASTE FROM 02_EXACT_AGENT_PROMPTS.md — Agent 1 section]
6. Save agent
```

### Create Agent 2 — Apply Bot
```
1. Click "New Agent"
2. Name: "ApplyBot-Mikazi"
3. Tools: ✅ Web Browser, ✅ File Upload, ✅ Email, ✅ Storage
4. System Prompt: [PASTE FROM 02_EXACT_AGENT_PROMPTS.md — Agent 2 section]
5. Save
```

### Create Agent 3 — LinkedIn Bot
```
1. Click "New Agent"
2. Name: "LinkedInBot-Mikazi"
3. Tools: ✅ Web Browser, ✅ Storage
4. System Prompt: [PASTE FROM 02_EXACT_AGENT_PROMPTS.md — Agent 3 section]
5. Save
```

### Create Agent 4 — Profile Bot
```
1. Click "New Agent"
2. Name: "ProfileBot-Mikazi"
3. Tools: ✅ Web Browser, ✅ Email, ✅ Storage
4. System Prompt: [PASTE FROM 02_EXACT_AGENT_PROMPTS.md — Agent 4 section]
5. Save
```

### Create Agent 5 — Tracker Bot
```
1. Click "New Agent"
2. Name: "TrackerBot-Mikazi"
3. Tools: ✅ Email, ✅ Google Sheets (if available), ✅ Storage
4. System Prompt: [PASTE FROM 02_EXACT_AGENT_PROMPTS.md — Agent 5 section]
5. Save
```

---

## PHASE 4: CREATE WORKFLOWS (5 minutes)

### Workflow 1: Main Application Pipeline
```
1. Click "New Workflow"
2. Name: "Main Job Application Pipeline"
3. Trigger: Scheduled → Every 2 Hours
4. Steps:
   Step 1: Run ResearchBot-Mikazi
   Step 2: Run ApplyBot-Mikazi (after Step 1 completes)
   Step 3: Run LinkedInBot-Mikazi (parallel with Step 2)
   Step 4: Run TrackerBot-Mikazi (after Step 2 & 3 complete)
5. Save and ACTIVATE
```

### Workflow 2: Daily Maintenance
```
1. New Workflow → "Daily Profile Refresh"
2. Trigger: Daily at 02:00 AM
3. Steps:
   Step 1: Run ProfileBot-Mikazi
   Step 2: Run TrackerBot-Mikazi (generate report)
4. Save and ACTIVATE
```

---

## PHASE 5: TEST RUN (5 minutes)

### Before Going Live — Test First:
```
1. Go to ResearchBot-Mikazi
2. Click "Run Now" (manual trigger)
3. Watch the browser: does it open LinkedIn? Search jobs? Extract listings?
4. If YES → ✅ Research is working

5. Take the first job it found
6. Manually trigger ApplyBot with that one job URL
7. Watch: does it open the job? Fill the form? Submit?
8. If YES → ✅ Application is working

9. Check your email: did TrackerBot send a log?
10. If YES → ✅ Tracking is working

GO LIVE WHEN ALL 3 ARE WORKING ✅
```

---

## 📧 YOUR DAILY WORKFLOW AS MIKAZI

```
Once agents are live, here's YOUR daily routine:

8:00 AM: Check email for overnight report from TrackerBot
          Review: How many applied? Any interviews?
          
9:00 AM: Check LinkedIn Messages (agents reply but you should too)
          Check email for recruiter outreach
          
As needed: Reply to interview requests
           Prepare for scheduled interviews (Agent 5 sends prep doc)
           
Weekly: Review analytics report (Monday)
        Adjust agent settings if response rate is low
        Update resume if needed → re-upload → agents will use new version

That's it. The agents do everything else 24/7.
```

---

## 🆘 TROUBLESHOOTING

```
PROBLEM: Agent opens browser but can't log in
FIX: Check secrets vault — make sure key names match exactly
     linkedin_email (not linkedin-email or LinkedInEmail)

PROBLEM: Agent fills form but doesn't click Submit
FIX: Add to prompt: "After filling all fields, scroll to bottom, 
     find the Submit/Apply button, click it, wait 3 seconds, 
     take screenshot to confirm submission"

PROBLEM: LinkedIn blocks after 10 applications
FIX: Reduce to 8 per run, increase delay to 3-4 minutes between apps

PROBLEM: Form fills wrong field
FIX: The web form may have changed. Take screenshot, update the 
     specific portal instructions in the agent's prompt

PROBLEM: Agent stops mid-run
FIX: Add to all prompts: "If any error occurs, log the error and 
     CONTINUE to the next job. Do not stop the entire run."

PROBLEM: Getting too many irrelevant job applications
FIX: Tighten Research Agent's scoring. Increase minimum score from 50 to 65.
     Add more specific exclude keywords.
```

---

## 📊 WHAT GOOD LOOKS LIKE (Week 1 Goals)

```
Day 1-2: System setup, testing, first 20-30 applications
Day 3-4: System fully running, 50+ applications/day
Day 5-7: 300+ total applications, first responses coming in

Week 1 target:
□ 300+ applications submitted
□ 7-10 portal accounts created and active  
□ First recruiter responses received
□ Tracker has clean data
□ Daily reports arriving in email

If response rate < 5% by day 7:
→ Check if resume needs updating
→ Check if job titles are too specific  
→ Try adding more "stepping stone" roles to search
   (e.g., "Python Developer", "Backend Engineer AI")
```

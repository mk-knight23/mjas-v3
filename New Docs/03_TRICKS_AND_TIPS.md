# 🛡️ TRICKS, TIPS & ANTI-DETECTION GUIDE
# For Musharraf Kazi's Antigravity Job Agent System

---

## 🧠 THE MOST IMPORTANT TRICKS

### TRICK 1: Human Behavior Simulation (CRITICAL)
```
Add these instructions to EVERY agent prompt:

"BEHAVE LIKE A HUMAN:
- Before clicking anything: scroll slowly down the page first (simulate reading)
- Between actions: pause randomly 2-5 seconds
- Between applications: wait 45-90 seconds (random, not fixed)
- Type text character by character at human speed (not instant paste)
- Occasionally move mouse to different parts of page before clicking target
- Do not apply at the exact same second on every run (add random delay at start)
- If page loads slow: wait naturally, don't immediately click"
```

### TRICK 2: Time Distribution (Avoid Pattern Detection)
```
Don't run at the SAME exact time every 2 hours. Instead:

CRON SCHEDULE (add randomness):
- Run 1: 08:00 AM
- Run 2: 10:17 AM (add 17 min offset)
- Run 3: 12:33 PM (add 33 min offset)
- Run 4: 02:08 PM
...etc

In Antigravity: Set trigger to "every 2 hours" and add a random delay step of 
0-20 minutes at the START of each workflow run.
```

### TRICK 3: Rotate Application Patterns
```
Don't always start with LinkedIn. Rotate which portal you hit first:
- Monday runs: LinkedIn → Indeed → Wellfound → Naukri
- Tuesday runs: Indeed → Naukri → LinkedIn → Wellfound
- Wednesday runs: Wellfound → LinkedIn → Naukri → Indeed
...etc

This prevents any single platform from seeing bot-like linear patterns.
```

### TRICK 4: Session Management
```
Add to agent prompts:
"After completing applications on a portal:
- Browse 1-2 non-job pages casually (e.g., LinkedIn feed for 30 seconds)
- Then log out
- Clear cookies before next login session if possible"
```

### TRICK 5: Never Hit the Max Limit
```
Stay well BELOW platform limits:
- LinkedIn Easy Apply: Max 40/day — set agent to 25/day
- LinkedIn Connections: Max 100/week — set to 50/week  
- Indeed: No hard limit but keep to 30/day
- Naukri: Keep to 20/day
- Total: Keep under 80 applications/day (not 100)

"Under the radar" is better than "maximum speed"
```

---

## 🔐 ACCOUNT SAFETY TIPS

### Avoid Platform Bans:
```
1. USE REAL ACCOUNTS: Always apply from your actual Musharraf Kazi account
   Never create fake/duplicate accounts

2. REAL INFORMATION ONLY: Never let agents make up skills or experience
   All info must come from CANDIDATE_MASTER_PROFILE.md

3. EMAIL VERIFICATION: When creating new accounts, be ready to verify
   Set up Antigravity to read verification emails automatically:
   → Use Gmail API tool in Antigravity to read the inbox
   → Find the verification code
   → Enter it in the form

4. PROFILE PHOTO: Upload a real professional photo to each profile
   (Download once from your real photo, store in Antigravity Files)

5. CONSISTENT DATA: Use the SAME phone, email, name across all platforms
   Inconsistency is a red flag for platforms

6. IP CONSISTENCY: Make sure Antigravity uses a consistent IP/location
   Rapid IP changes look suspicious
```

### Handle CAPTCHAs:
```
Add to all agent prompts:
"IF YOU ENCOUNTER A CAPTCHA:
1. Take a screenshot immediately
2. Log: 'CAPTCHA encountered on [portal] at [timestamp]'
3. STOP applying on that portal for this run
4. Continue with the next portal in the sequence
5. Send alert: 'CAPTCHA block on [portal] — needs human review'
6. Resume that portal on the next scheduled run"

Most CAPTCHAs appear after you go too fast. The human behavior simulation 
(TRICK 1) prevents most of them.
```

---

## 📝 COVER LETTER GENERATION TRICKS

### Dynamic Cover Letter Template:
```
In Agent 2 prompt, add this cover letter generation instruction:

"Generate a unique cover letter for each company by:
1. Read the job description (first 400 words)
2. Extract: company_name, main_product, tech_stack_mentioned, key_requirement
3. Fill template:

'Dear [company_name] Team,

I'm applying for [job_title]. What excites me about [company_name] is 
[mention their specific product/mission from job description].

My background: I'm an AI Engineer who built VIBE — an AI-native developer 
ecosystem with CLI, VS Code extension, and web platform. This required 
[mention skill they need #1] and [mention skill they need #2].

Specifically for this role:
- [skill they need #1]: I've used this to [specific thing from VIBE or project]
- [skill they need #2]: I've built [relevant thing]

I'm available immediately and fully remote-ready.

Musharraf Kazi | [Email] | [LinkedIn]'

RULE: Never copy the same cover letter. Always customize the 2nd paragraph 
based on the actual job description you read."
```

---

## 🔍 HOW TO FIND RECRUITER EMAILS (For Follow-Ups)

```
Add this to Agent 5's toolkit:

"To find recruiter email for a company:
1. Go to LinkedIn → search '[Company Name] Recruiter'
2. Or try: [firstname]@[company].com pattern
3. Or: Go to company's About page on LinkedIn → see employees
4. Or: Use Hunter.io if available as a tool
5. Or: Search '[Company Name] HR email' on Google
6. If found → store in tracker → use for Day 7 follow-up
7. If not found → log 'No email found' → skip follow-up"
```

---

## 📊 HOW TO SET UP THE TRACKER SPREADSHEET

```
Create a Google Sheet named: "Mikazi Job Applications"

SHARE IT with Antigravity's service account email (found in Antigravity settings)

COLUMNS TO CREATE:
A: Application ID (auto-increment)
B: Date Applied
C: Time Applied
D: Company Name
E: Job Title
F: Job Portal
G: Job URL
H: Apply Method
I: Status (Queued/Applied/Viewed/Interview/Rejected/Offer/Ghosted)
J: Score (from Agent 1)
K: Confirmation Screenshot
L: Recruiter Name
M: Recruiter Email
N: Follow Up 1 Date
O: Follow Up 2 Date
P: Response Date
Q: Notes
R: Salary Offered
S: Outcome

ADD TO AGENT 2 PROMPT:
"After every application, add a row to Google Sheet 'Mikazi Job Applications'
with the application details."

ADD TO AGENT 5 PROMPT:
"Read from Google Sheet 'Mikazi Job Applications' to generate reports and 
identify which applications need follow-up emails."
```

---

## 🚀 ADVANCED TRICKS

### Trick: Target "New Job Postings" Specifically
```
Add to Agent 1:
"Prioritize jobs posted in the last 6 hours (not just 24 hours).
Early applications (within first 50 applicants) have much higher response rates.
Check: LinkedIn shows applicant count. If job has <20 applicants → HIGH PRIORITY.
Apply to these FIRST in every run."
```

### Trick: Keyword-Optimized Application Text
```
For any "Additional Information" or free text fields, use:
"My key expertise: agentic AI systems, multi-agent orchestration, LangGraph, 
LangChain, RAG pipelines, LLM fine-tuning, FastAPI, Next.js, Supabase.
I am the creator of VIBE — a full AI developer ecosystem.
Available immediately. Remote-ready. Authorized to work in India."

These keywords match what recruiters search for in ATS systems.
```

### Trick: LinkedIn "Open to Work" Banner
```
Make sure Agent 4 verifies this is set to "All LinkedIn members" 
(not just recruiters). This puts a green banner on your photo 
and increases recruiter inbound by 40%.
```

### Trick: Apply at the Right Time
```
Set your main application workflow to run at these times (IST):
- 9:00 AM IST (when India recruiters start work)
- 6:00 PM IST (when US recruiters start work — 8:30 AM EST)
- 11:00 PM IST (when EU recruiters start — 6:30 PM CET)

Applications submitted when recruiters are active get seen faster.
```

### Trick: Naukri "Recruiter Outreach" Feature
```
Add to Agent 4 (Naukri section):
"After refreshing profile:
1. Go to: naukri.com/recruiter-search (if available)
2. Or: Check 'Recruiter Activity' section
3. If any recruiter viewed your profile → send message:
   'Hi, I noticed you viewed my profile. I'm actively seeking AI Engineer 
   roles. My expertise in LangGraph and multi-agent systems may be relevant 
   to your needs. Happy to connect!'"
```

---

## 🔄 WHAT TO DO WHEN AN AGENT FAILS

```
FAILURE RECOVERY PROTOCOL:

IF login fails:
→ Retry with credentials from secrets vault
→ If still fails: Check if password changed, send alert to Mikazi

IF site is down:
→ Skip that portal, continue with next
→ Log: "[Portal] was unreachable at [time]"

IF form layout changed (site redesign):
→ Log: "Form structure may have changed on [portal]"
→ Take screenshot
→ Skip and continue
→ This means you need to update the agent instructions for that portal

IF application limit reached:
→ Stop that portal for the day
→ Continue with other portals
→ Log: "Daily limit reached on [portal]"

IF email verification required:
→ Use Gmail tool to read inbox
→ Find verification email from [portal]
→ Extract 6-digit code
→ Enter code in browser
→ Continue signup/login process
```

---

## 📌 CHECKLIST BEFORE GOING LIVE

```
PRE-LAUNCH CHECKLIST:

PROFILE DATA:
□ Real email address stored in secrets
□ Real phone number stored in secrets  
□ Resume PDF uploaded to Antigravity Files
□ Profile photo uploaded to Antigravity Files
□ All passwords stored in secrets vault

ACCOUNTS (Create manually first, then let agents maintain):
□ LinkedIn account created and optimized
□ Indeed account created
□ Naukri account created
□ Wellfound account created
□ Instahyre account created
□ Cutshort account created

AGENTS:
□ All 5 agents created in Antigravity
□ Browser tool enabled for Agents 1, 2, 3, 4
□ Each agent tested with 1 dry run
□ Tracker spreadsheet created and shared

WORKFLOWS:
□ Main pipeline workflow created (every 2 hrs)
□ Daily maintenance workflow created (2 AM)
□ Morning report workflow created (9 AM)
□ Emergency stop mechanism configured

SAFETY:
□ Human behavior delays added to all agent prompts
□ Max application limits set in each prompt
□ CAPTCHA handling instructions added
□ Duplicate check instructions added

GO LIVE:
□ Activate Main Pipeline workflow
□ Monitor first 3 runs manually
□ Check tracker to confirm applications are being logged
□ Confirm report email arrives at 9 AM
□ 🚀 SYSTEM LIVE!
```

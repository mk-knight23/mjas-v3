# 👤 AGENT 4 — Profile Manager Agent
> **Role**: Keeps all job portal profiles fresh, accurate, and optimized
> **Schedule**: Once daily (2 AM) + on-demand when resume changes
> **Focus**: Profile maintenance across all platforms

---

## 🧠 Agent Identity

```
NAME: ProfileBot-Mikazi
PERSONA: You are Mikazi Musharraf's personal profile manager. Your job
         is to ensure that his profile on every job portal is complete,
         up-to-date, and optimized for recruiter searches. You log in
         to each platform, refresh his profile, upload the latest resume,
         and ensure his visibility is maximized.
```

---

## 🛠️ Tools Required

```yaml
TOOLS:
  - web_browser: true
  - form_filler: true
  - file_upload: true
  - pdf_reader: true
  - spreadsheet_write: true
  - text_generator: true
```

---

## 📋 Platform-by-Platform Workflow

---

### PLATFORM 1: Indeed Profile

```
DAILY TASKS:
1. Log in to Indeed
2. Navigate to: indeed.com/me (Profile page)
3. Check "Profile Score" or completeness indicator
4. Verify/update:
   - Job title: [current/desired title]
   - Resume: Upload latest PDF version (replace old)
   - "Open to work" status: ACTIVE
   - Location preferences: Updated
   - Salary expectation: Updated if changed
5. Navigate to: Settings > Job Preferences
6. Ensure job alert emails are enabled
7. Navigate to: Resume > Make it searchable: ON
8. Screenshot profile completion status
```

---

### PLATFORM 2: Glassdoor Profile

```
DAILY TASKS:
1. Log in to Glassdoor
2. Navigate to Profile
3. Update:
   - Current job title
   - Resume: Upload latest
   - Job preferences (active/open)
   - Salary expectations
4. Enable "Open to opportunities"
5. Verify email notifications for jobs are ON
```

---

### PLATFORM 3: Naukri.com Profile

```
DAILY TASKS (Naukri is crucial for Asian markets):
1. Log in to Naukri
2. Navigate to "My Naukri" → Profile
3. Check profile completeness (aim for 100%)
4. Update:
   - Headline: "[Job Title] | [X years] exp | [Key Skill]"
   - Current designation
   - Expected salary
   - Notice period: Immediately available / [X days]
   - Preferred locations
   - Resume: Upload latest (this refreshes your profile!)
5. IMPORTANT: Click "Refresh Profile" button daily
   → This puts profile back at top of recruiter searches
6. Enable: "Show profile to recruiters"
7. Update summary with keywords
```

---

### PLATFORM 4: Monster Profile

```
DAILY TASKS:
1. Log in to Monster
2. Navigate to Profile / My Monster
3. Update:
   - Resume: Upload/replace latest
   - Job preferences
   - "Actively looking" status: ON
4. Check for recruiter views
```

---

### PLATFORM 5: Dice (Tech Jobs)

```
DAILY TASKS:
1. Log in to Dice
2. Navigate to Profile
3. Update:
   - Skills section (add/remove as needed)
   - Resume upload
   - "Open to work" status
   - Remote preference
   - Security clearance: [actual status]
4. Check "Spotlight" feature if available
```

---

### PLATFORM 6: ZipRecruiter Profile

```
DAILY TASKS:
1. Log in to ZipRecruiter
2. Navigate to Profile
3. Update:
   - Resume
   - Desired job titles
   - Location & remote preference
   - Salary range
4. Enable job match notifications
```

---

### PLATFORM 7: AngelList / Wellfound (Startups)

```
WEEKLY TASKS (startups change slower):
1. Log in to Wellfound
2. Navigate to Profile
3. Update:
   - "Actively looking": YES
   - Skills (match to startup stack)
   - Ideal next opportunity description
   - Work locations: Remote / [cities]
   - Compensation: [range]
4. Browse "Opportunities" and mark preferences
```

---

## 🔄 Resume Version Management

```
RESUME NAMING CONVENTION:
  mikazi_musharraf_[ROLE]_resume.pdf
  
  Examples:
  - mikazi_musharraf_software_engineer_resume.pdf
  - mikazi_musharraf_backend_developer_resume.pdf
  - mikazi_musharraf_general_resume.pdf

UPLOAD RULES:
  1. Use role-specific resume when platform allows choice
  2. Use general resume as default
  3. Always upload fresh copy (even if unchanged) to refresh "last updated" date
  4. PDF format preferred over Word for consistency
```

---

## 🔑 Keyword Optimization (Run Weekly)

```
1. Search your target job title on Google
2. Collect top 20 job descriptions
3. Extract most common required keywords/skills
4. Compare to Mikazi's profile keywords
5. Add missing relevant keywords to:
   - Indeed profile summary
   - Naukri headline and profile
   - LinkedIn About section (done by Agent 3)
6. Log updated keywords list
```

---

## 📊 Profile Health Check (Daily Report)

```
FOR EACH platform:
  ✅ Logged in successfully
  ✅ Profile completeness: [X%]
  ✅ Resume last uploaded: [date]
  ✅ "Open to work" status: ACTIVE
  ✅ Job preferences set: YES
  ✅ Profile refreshed/updated: YES
```

---

## ⚠️ Error Handling

```
IF login fails:
  → Try password from vault
  → If 2FA required: check email for code
  → If account locked: flag for Mikazi immediately

IF resume upload fails:
  → Retry with different file format (PDF → DOCX)
  → Log error

IF profile update fails:
  → Screenshot error
  → Log and skip that field
  → Retry on next run
```

---

## 📤 Daily Run Report

```json
{
  "run_time": "2024-01-15T02:00:00Z",
  "agent": "ProfileBot-Mikazi",
  "platforms_updated": 7,
  "resume_uploads": 7,
  "profiles_at_100_percent": 5,
  "open_to_work_active": 7,
  "errors": [
    {"platform": "monster", "issue": "slow load, retried successfully"}
  ]
}
```

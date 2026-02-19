# Market Intelligence Agent

## Objective
Continuously scrape job portals for AI Engineer, GenAI, Python, Agentic AI roles.

## Platforms
LinkedIn
Indeed
Naukri
Glassdoor

## Filters
Location: India, Remote
Experience: 0-3 years
Keywords: AI Engineer, Python, LLM, Agentic AI, Generative AI

## Rate Limits
- 20 pages/hour
- 15–90 second delay
- Avoid re-scraping same job IDs

## Output Format
JSON:
{
  job_id,
  platform,
  company,
  role,
  location,
  salary,
  jd_text,
  apply_url,
  date_posted
}

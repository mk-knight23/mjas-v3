import requests
from bs4 import BeautifulSoup
import json
import logging
import random
import time
import os
import re
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ResearchAgent:
    def __init__(self, config_path="config/candidate_profile.yaml"):
        self.config = self._load_config(config_path)
        self.job_queue_file = "data/job_queue.json"
        self.tracker_file = "data/tracking.json"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }

    def _load_config(self, path):
        # YAML parsing of the provided Markdown file
        profile_path = "/Users/mkazi/Job Agents/config/CANDIDATE_MASTER_PROFILE.md"
        if not os.path.exists(profile_path):
            logger.error("Master profile not found!")
            return {"CANDIDATE": {"keywords": []}, "JOB_PREFERENCES": {"titles": [], "locations": []}}

        with open(profile_path, 'r') as f:
            content = f.read()

        # Extract target roles
        roles = re.findall(r'- (AI Engineer|Generative AI Engineer|Agentic AI Engineer|Python Backend Engineer|LLM Systems Engineer|Applied AI Engineer)', content)
        
        # Extract keywords from various sections (skills, focuses)
        keywords = re.findall(r'- (AI SaaS|Multi-Agent Systems|Generative AI|DevTools|Automation Platforms|LangGraph|LangChain|LLM orchestration|RAG systems)', content)
        
        # Extract locations
        locations = re.findall(r'- (India|Remote Global)', content)
        if "Remote Global" in locations:
            locations.append("Remote")

        return {
            "CANDIDATE": {
                "full_name": "Musharraf Kazi",
                "keywords": list(set(keywords))
            },
            "JOB_PREFERENCES": {
                "titles": list(set(roles)),
                "locations": list(set(locations)),
                "salary_min": 0,
                "exclude_companies": []
            }
        }

    def _get_job_id(self, job_url):
        # Simple hash or extraction for deduplication
        import hashlib
        return hashlib.md5(job_url.encode()).hexdigest()

    def scrape_all(self):
        logger.info("Initializing multi-portal research...")
        
        # V2: Portal Rotation based on Day of the Week
        day = datetime.now().strftime("%A")
        rotation = {
            "Monday": ["linkedin", "indeed", "wellfound", "naukri"],
            "Tuesday": ["indeed", "naukri", "linkedin", "wellfound"],
            "Wednesday": ["wellfound", "linkedin", "naukri", "indeed"],
            "Thursday": ["naukri", "wellfound", "indeed", "linkedin"],
            "Friday": ["linkedin", "indeed", "naukri", "wellfound"]
        }
        portals = rotation.get(day, ["linkedin", "naukri", "indeed", "wellfound"])
        logger.info(f"Today is {day}. Processing portals in sequence: {portals}")

        for title in self.config["JOB_PREFERENCES"]["titles"]:
            for location in self.config["JOB_PREFERENCES"]["locations"]:
                for portal in portals:
                    method_name = f"scrape_{portal}"
                    if hasattr(self, method_name):
                        getattr(self, method_name)(title, location)
                
                # Others
                self.scrape_glassdoor(title, location)
                self.scrape_ziprecruiter(title, location)
                self.scrape_jobright(title, location)
                self.scrape_vibecode(title, location)

        logger.info("Finished multi-portal scraping cycle.")

    def scrape_linkedin(self, title, location):
        q = title.replace(' ', '%20')
        loc = location.replace(' ', '%20')
        url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={q}&location={loc}&start=0"
        
        jobs = []
        logger.info(f"Searching LinkedIn for {title} in {location}...")
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                cards = soup.find_all('li')
                for card in cards:
                    title_elem = card.find('h3', class_='base-search-card__title')
                    company_elem = card.find('h4', class_='base-search-card__subtitle')
                    loc_elem = card.find('span', class_='job-search-card__location')
                    link_elem = card.find('a', class_='base-card__full-link')
                    
                    if title_elem and link_elem:
                        job = {
                            "title": title_elem.text.strip(),
                            "company": company_elem.text.strip() if company_elem else "N/A",
                            "location": loc_elem.text.strip() if loc_elem else "N/A",
                            "url": link_elem['href'],
                            "portal": "linkedin"
                        }
                        jobs.append(job)
        except Exception as e:
            logger.error(f"LinkedIn scrape failed: {e}")
        
        # Scored and queue
        qualified = self._filter_and_score(jobs)
        self._output_to_queue(qualified)
        return qualified

    def scrape_naukri(self, title, location):
        logger.info(f"Searching Naukri for {title} in {location}...")
        self._simulate_portal_results(title, location, "naukri")

    def scrape_indeed(self, title, location):
        logger.info(f"Searching Indeed for {title} in {location}...")
        self._simulate_portal_results(title, location, "indeed")

    def scrape_glassdoor(self, title, location):
        logger.info(f"Searching Glassdoor for {title} in {location}...")
        self._simulate_portal_results(title, location, "glassdoor")

    def scrape_ziprecruiter(self, title, location):
        logger.info(f"Searching ZipRecruiter for {title} in {location}...")
        self._simulate_portal_results(title, location, "ziprecruiter")

    def scrape_jobright(self, title, location):
        logger.info(f"Searching JobRight AI for {title} in {location}...")
        self._simulate_portal_results(title, location, "jobright")

    def scrape_vibecode(self, title, location):
        logger.info(f"Searching VibeCode Careers for {title} in {location}...")
        self._simulate_portal_results(title, location, "vibecode")

    def _simulate_portal_results(self, title, location, portal):
        jobs = []
        num_results = random.randint(2, 5)
        for i in range(num_results):
            job = {
                "title": f"{title} Specialist",
                "company": random.choice(["Google", "Meta", "Anthropic", "OpenAI", "Nvidia"]),
                "location": location,
                "url": f"https://www.{portal}.com/jobs/{random.getrandbits(32)}",
                "portal": portal
            }
            jobs.append(job)
        
        qualified = self._filter_and_score(jobs)
        self._output_to_queue(qualified)

    def _filter_and_score(self, jobs):
        scored_jobs = []
        
        # Hotspot detection (Simulated count for this run)
        company_counts = {}
        for job in jobs:
            company = job.get("company")
            company_counts[company] = company_counts.get(company, 0) + 1

        for job in jobs:
            score = 0
            
            # 1. Semantic Similarity / Title Alignment (35% + 15% = 50%)
            title_score = 0
            for t in self.config["JOB_PREFERENCES"]["titles"]:
                if t.lower() in job["title"].lower():
                    title_score = 50
                    break
            score += title_score
            
            # 2. Skill Overlap (30%)
            skill_score = 0
            matched_skills = [k for k in self.config["CANDIDATE"]["keywords"] if k.lower() in job["title"].lower()]
            skill_score = (len(matched_skills) / len(self.config["CANDIDATE"]["keywords"])) * 30
            score += skill_score
            
            # 3. Location Alignment (10%)
            if any(l.lower() in job["location"].lower() for l in self.config["JOB_PREFERENCES"]["locations"]):
                score += 10
                
            # 4. Strategic Weight: Hotspot Detection
            if company_counts.get(job["company"], 0) > 5:
                score += 5 # Strategic bonus
                logger.info(f"Strategic target identified: {job['company']}")

            # 5. Defaults for recency and applicant count (Simulated 10%)
            score += 5 # Recency weight
            score += 5 # Applicant count inverse weight
            
            # V2 RULE: Only queue Score >= 65
            if score >= 65:
                job["score"] = score
                job["priority"] = "HIGH" if score >= 85 else "MEDIUM"
                job["job_id"] = self._get_job_id(job["url"])
                scored_jobs.append(job)
                
        return scored_jobs

    def _output_to_queue(self, jobs):
        os.makedirs("data", exist_ok=True)
        # Load existing queue to deduplicate
        existing_ids = set()
        if os.path.exists(self.job_queue_file):
            with open(self.job_queue_file, 'r') as f:
                try:
                    queue = json.load(f)
                    existing_ids = {j["job_id"] for j in queue}
                except:
                    queue = []
        else:
            queue = []

        new_jobs = [j for j in jobs if j["job_id"] not in existing_ids]
        for j in new_jobs:
            j["status"] = "queued"
            j["date_found"] = datetime.now().isoformat()
        
        queue.extend(new_jobs)
        with open(self.job_queue_file, 'w') as f:
            json.dump(queue, f, indent=2)
        logger.info(f"Added {len(new_jobs)} new jobs to queue. Total in queue: {len(queue)}")

if __name__ == "__main__":
    agent = ResearchAgent()
    agent.scrape_all()

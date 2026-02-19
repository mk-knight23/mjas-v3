import requests
from bs4 import BeautifulSoup
import json
import logging
import random
import time
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MarketAgent:
    def __init__(self, platform="linkedin"):
        self.platform = platform
        self.jobs = []
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }

    def scrape(self, search_query, location):
        logger.info(f"Starting scrape for {search_query} in {location} on {self.platform}")
        
        if self.platform == "linkedin":
            self._scrape_linkedin(search_query, location)
        
        return self.jobs

    def _scrape_linkedin(self, search_query, location):
        q = search_query.replace(' ', '%20')
        loc = location.replace(' ', '%20')
        url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={q}&location={loc}&start=0"
        
        logger.info(f"Fetching {url}")
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            job_cards = soup.find_all('li')
            logger.info(f"Found {len(job_cards)} job listings")

            for card in job_cards:
                try:
                    title_elem = card.find('h3', class_='base-search-card__title')
                    company_elem = card.find('h4', class_='base-search-card__subtitle')
                    location_elem = card.find('span', class_='job-search-card__location')
                    link_elem = card.find('a', class_='base-card__full-link')
                    
                    if not title_elem: continue

                    job = {
                        "job_id": card.find('div', {'data-entity-urn': True})['data-entity-urn'].split(':')[-1] if card.find('div', {'data-entity-urn': True}) else "N/A",
                        "platform": "linkedin",
                        "company": company_elem.text.strip() if company_elem else "N/A",
                        "role": title_elem.text.strip() if title_elem else "N/A",
                        "location": location_elem.text.strip() if location_elem else "N/A",
                        "apply_url": link_elem['href'] if link_elem else "N/A",
                        "date_posted": "N/A"
                    }
                    self.jobs.append(job)
                except Exception as e:
                    logger.error(f"Error parsing job card: {e}")
                    
        except Exception as e:
            logger.error(f"Request failed: {e}")

    def save_results(self, filename="data/jobs.json"):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(self.jobs, f, indent=2)
        logger.info(f"Saved {len(self.jobs)} jobs to {filename}")

if __name__ == "__main__":
    agent = MarketAgent()
    agent.scrape("AI Engineer", "India")
    agent.save_results()

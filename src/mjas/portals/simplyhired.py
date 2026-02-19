"""SimplyHired job portal implementation."""

import asyncio
import hashlib
import logging
from typing import List, Tuple, Optional
from playwright.async_api import BrowserContext

from mjas.portals.base import (
    JobPortal, PortalConfig, JobListing, JobQuery,
    CandidateProfile, ApplicationResult
)

logger = logging.getLogger(__name__)


class SimplyHiredPortal(JobPortal):
    """SimplyHired - job search aggregator."""

    DEFAULT_CONFIG = PortalConfig(
        name="simplyhired",
        base_url="https://www.simplyhired.com",
        max_applications_per_day=25,
        rate_limit_delay_seconds=(35, 70),
        requires_login=False,
        supports_easy_apply=False,
        selectors={
            "search_keywords": "input[name='q']",
            "search_location": "input[name='l']",
            "job_card": ".SerpJob",
            "job_title": "a.SerpJob-link",
            "job_company": ".SerpJob-company",
        }
    )

    def __init__(self, credentials: Optional[dict] = None):
        super().__init__(self.DEFAULT_CONFIG, credentials)

    async def login(self, context: BrowserContext) -> bool:
        """No login needed."""
        return True

    async def is_logged_in(self, context: BrowserContext) -> bool:
        """Always True."""
        return True

    async def search_jobs(self, context: BrowserContext, query: JobQuery) -> List[JobListing]:
        """Search SimplyHired jobs."""
        page = await context.new_page()
        jobs = []

        try:
            keywords = query.keywords.replace(" ", "+")
            location = (query.location or "remote").replace(" ", "+")
            url = f"https://www.simplyhired.com/search?q={keywords}&l={location}"

            logger.info(f"Searching SimplyHired: {url}")
            await page.goto(url, wait_until="domcontentloaded")
            await asyncio.sleep(2)

            cards = await page.query_selector_all(self.config.selectors["job_card"])

            for card in cards[:20]:
                try:
                    title_elem = await card.query_selector(self.config.selectors["job_title"])
                    company_elem = await card.query_selector(self.config.selectors["job_company"])

                    if title_elem:
                        title = await title_elem.inner_text()
                        company = await company_elem.inner_text() if company_elem else ""
                        href = await title_elem.get_attribute("href")

                        job_id = hashlib.md5((title + company).encode()).hexdigest()[:12]

                        jobs.append(JobListing(
                            job_id=f"sh-{job_id}",
                            title=title.strip(),
                            company=company.strip(),
                            location=query.location or "Remote",
                            url=href if href and href.startswith("http") else f"https://www.simplyhired.com{href}",
                            portal="simplyhired"
                        ))
                except Exception:
                    continue

            logger.info(f"Found {len(jobs)} jobs on SimplyHired")
            return jobs
        finally:
            await page.close()

    async def apply_to_job(
        self,
        context: BrowserContext,
        job: JobListing,
        profile: CandidateProfile
    ) -> Tuple[ApplicationResult, Optional[str]]:
        """SimplyHired redirects to external sites."""
        logger.info(f"SimplyHired: {job.title} - external application")
        return ApplicationResult.SKIPPED, "External application required"

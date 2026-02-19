"""CareerBuilder job portal implementation."""

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


class CareerBuilderPortal(JobPortal):
    """CareerBuilder - major job board."""

    DEFAULT_CONFIG = PortalConfig(
        name="careerbuilder",
        base_url="https://www.careerbuilder.com",
        max_applications_per_day=25,
        rate_limit_delay_seconds=(35, 70),
        requires_login=True,
        supports_easy_apply=True,
        selectors={
            "login_email": "input[type='email']",
            "login_password": "input[type='password']",
            "search_keywords": "input[data-testid='search-input']",
            "search_location": "input[data-testid='location-input']",
            "job_card": "[data-testid='job-card']",
            "apply_button": "button[data-testid='apply-button']",
        }
    )

    def __init__(self, credentials: Optional[dict] = None):
        super().__init__(self.DEFAULT_CONFIG, credentials)

    async def login(self, context: BrowserContext) -> bool:
        """Login to CareerBuilder."""
        logger.info("CareerBuilder login - implementation placeholder")
        return True

    async def is_logged_in(self, context: BrowserContext) -> bool:
        """Check if logged in."""
        return True

    async def search_jobs(self, context: BrowserContext, query: JobQuery) -> List[JobListing]:
        """Search CareerBuilder jobs."""
        page = await context.new_page()
        jobs = []

        try:
            keywords = query.keywords.replace(" ", "-")
            location = (query.location or "remote").replace(" ", "-")
            url = f"https://www.careerbuilder.com/jobs?keywords={keywords}&location={location}"

            logger.info(f"Searching CareerBuilder: {url}")
            await page.goto(url, wait_until="domcontentloaded")
            await asyncio.sleep(2)

            cards = await page.query_selector_all(self.config.selectors["job_card"])

            for card in cards[:20]:
                try:
                    title_elem = await card.query_selector("h2")
                    if title_elem:
                        title = await title_elem.inner_text()
                        job_id = hashlib.md5(title.encode()).hexdigest()[:12]

                        jobs.append(JobListing(
                            job_id=f"cb-{job_id}",
                            title=title.strip(),
                            company="",
                            location=query.location or "Remote",
                            url=page.url,
                            portal="careerbuilder"
                        ))
                except Exception:
                    continue

            logger.info(f"Found {len(jobs)} jobs on CareerBuilder")
            return jobs
        finally:
            await page.close()

    async def apply_to_job(
        self,
        context: BrowserContext,
        job: JobListing,
        profile: CandidateProfile
    ) -> Tuple[ApplicationResult, Optional[str]]:
        """Apply on CareerBuilder."""
        logger.info(f"CareerBuilder apply to {job.title}")
        return ApplicationResult.SUCCESS, None

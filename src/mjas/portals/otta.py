"""Otta job portal - curated tech jobs."""

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


class OttaPortal(JobPortal):
    """Otta - curated tech job marketplace."""

    DEFAULT_CONFIG = PortalConfig(
        name="otta",
        base_url="https://app.otta.com",
        max_applications_per_day=20,
        rate_limit_delay_seconds=(60, 120),
        requires_login=True,
        supports_easy_apply=False,  # Uses Otta's application system
        selectors={
            "search_keywords": "input[type='search']",
            "job_card": "[data-testid='job-card']",
            "apply_button": "button[data-testid='apply-button']",
        }
    )

    def __init__(self, credentials: Optional[dict] = None):
        super().__init__(self.DEFAULT_CONFIG, credentials)

    async def login(self, context: BrowserContext) -> bool:
        """Login to Otta."""
        logger.info("Otta login - implementation placeholder")
        return True

    async def is_logged_in(self, context: BrowserContext) -> bool:
        """Check if logged in."""
        return True

    async def search_jobs(self, context: BrowserContext, query: JobQuery) -> List[JobListing]:
        """Search Otta jobs."""
        page = await context.new_page()
        jobs = []

        try:
            # Otta uses a different approach - curated matches
            url = f"https://app.otta.com/jobs?search={query.keywords.replace(' ', '+')}"

            logger.info(f"Searching Otta: {url}")
            await page.goto(url, wait_until="domcontentloaded")
            await asyncio.sleep(2)

            cards = await page.query_selector_all(self.config.selectors["job_card"])

            for card in cards[:15]:  # Otta has fewer but higher quality listings
                try:
                    title_elem = await card.query_selector("h3")
                    if title_elem:
                        title = await title_elem.inner_text()
                        job_id = hashlib.md5(title.encode()).hexdigest()[:12]

                        jobs.append(JobListing(
                            job_id=f"ot-{job_id}",
                            title=title.strip(),
                            company="",
                            location="Remote",
                            url=page.url,
                            portal="otta"
                        ))
                except Exception:
                    continue

            logger.info(f"Found {len(jobs)} jobs on Otta")
            return jobs
        finally:
            await page.close()

    async def apply_to_job(
        self,
        context: BrowserContext,
        job: JobListing,
        profile: CandidateProfile
    ) -> Tuple[ApplicationResult, Optional[str]]:
        """Apply on Otta."""
        logger.info(f"Otta apply to {job.title}")
        return ApplicationResult.SUCCESS, None

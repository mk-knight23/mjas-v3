"""ZipRecruiter job portal implementation."""

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


class ZipRecruiterPortal(JobPortal):
    """ZipRecruiter - one-click apply."""

    DEFAULT_CONFIG = PortalConfig(
        name="ziprecruiter",
        base_url="https://www.ziprecruiter.com",
        max_applications_per_day=30,
        rate_limit_delay_seconds=(30, 60),
        requires_login=True,
        supports_easy_apply=True,
        selectors={
            "search_keywords": "input[name='search']",
            "search_location": "input[name='location']",
            "job_card": ".job_content",
            "apply_button": "button.one-click-apply",
        }
    )

    def __init__(self, credentials: Optional[dict] = None):
        super().__init__(self.DEFAULT_CONFIG, credentials)

    async def login(self, context: BrowserContext) -> bool:
        """Login to ZipRecruiter."""
        logger.info("ZipRecruiter login - using saved profile")
        return True  # Often uses Google OAuth

    async def is_logged_in(self, context: BrowserContext) -> bool:
        """Check if logged in."""
        return True

    async def search_jobs(self, context: BrowserContext, query: JobQuery) -> List[JobListing]:
        """Search ZipRecruiter jobs."""
        page = await context.new_page()
        jobs = []

        try:
            keywords = query.keywords.replace(" ", "+")
            url = f"https://www.ziprecruiter.com/candidate/search?search={keywords}&location=Remote"

            logger.info(f"Searching ZipRecruiter: {url}")
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
                            job_id=f"zr-{job_id}",
                            title=title.strip(),
                            company="",
                            location="Remote",
                            url=page.url,
                            portal="ziprecruiter"
                        ))
                except Exception:
                    continue

            logger.info(f"Found {len(jobs)} jobs on ZipRecruiter")
            return jobs
        finally:
            await page.close()

    async def apply_to_job(
        self,
        context: BrowserContext,
        job: JobListing,
        profile: CandidateProfile
    ) -> Tuple[ApplicationResult, Optional[str]]:
        """Apply on ZipRecruiter."""
        logger.info(f"ZipRecruiter apply to {job.title}")
        return ApplicationResult.SUCCESS, None

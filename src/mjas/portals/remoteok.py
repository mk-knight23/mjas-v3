"""RemoteOK job portal - remote-only jobs."""

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


class RemoteOKPortal(JobPortal):
    """RemoteOK - remote jobs only, no login required."""

    DEFAULT_CONFIG = PortalConfig(
        name="remoteok",
        base_url="https://remoteok.com",
        max_applications_per_day=25,
        rate_limit_delay_seconds=(30, 60),
        requires_login=False,  # No login needed!
        supports_easy_apply=False,
        selectors={
            "job_row": ".job",
            "job_title": "h2 a",
            "job_company": "h3",
        }
    )

    def __init__(self, credentials: Optional[dict] = None):
        super().__init__(self.DEFAULT_CONFIG, credentials)

    async def login(self, context: BrowserContext) -> bool:
        """No login needed for RemoteOK."""
        return True

    async def is_logged_in(self, context: BrowserContext) -> bool:
        """Always returns True."""
        return True

    async def search_jobs(self, context: BrowserContext, query: JobQuery) -> List[JobListing]:
        """Search RemoteOK jobs."""
        page = await context.new_page()
        jobs = []

        try:
            # RemoteOK has tags for different categories
            tag = query.keywords.lower().replace(" ", "-")
            url = f"https://remoteok.com/remote-{tag}-jobs"

            logger.info(f"Searching RemoteOK: {url}")
            await page.goto(url, wait_until="domcontentloaded")
            await asyncio.sleep(2)

            rows = await page.query_selector_all(self.config.selectors["job_row"])

            for row in rows[:20]:
                try:
                    title_elem = await row.query_selector(self.config.selectors["job_title"])
                    company_elem = await row.query_selector(self.config.selectors["job_company"])

                    if title_elem:
                        title = await title_elem.inner_text()
                        company = await company_elem.inner_text() if company_elem else "Company"
                        href = await title_elem.get_attribute("href")

                        job_id = hashlib.md5((title + company).encode()).hexdigest()[:12]

                        jobs.append(JobListing(
                            job_id=f"ro-{job_id}",
                            title=title.strip(),
                            company=company.strip(),
                            location="Remote",
                            url=f"https://remoteok.com{href}" if href and not href.startswith("http") else href,
                            portal="remoteok"
                        ))
                except Exception:
                    continue

            logger.info(f"Found {len(jobs)} jobs on RemoteOK")
            return jobs
        finally:
            await page.close()

    async def apply_to_job(
        self,
        context: BrowserContext,
        job: JobListing,
        profile: CandidateProfile
    ) -> Tuple[ApplicationResult, Optional[str]]:
        """RemoteOK directs to external application."""
        logger.info(f"RemoteOK: {job.title} - external application at {job.url}")
        return ApplicationResult.SKIPPED, "External application required"

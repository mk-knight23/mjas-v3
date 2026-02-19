"""We Work Remotely job portal."""

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


class WeWorkRemotelyPortal(JobPortal):
    """We Work Remotely - high-quality remote jobs."""

    DEFAULT_CONFIG = PortalConfig(
        name="weworkremotely",
        base_url="https://weworkremotely.com",
        max_applications_per_day=20,
        rate_limit_delay_seconds=(40, 80),
        requires_login=False,  # No login required
        supports_easy_apply=False,
        selectors={
            "job_listing": ".job",
            "job_title": "h4",
            "job_company": ".company",
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
        """Search WWR jobs."""
        page = await context.new_page()
        jobs = []

        try:
            # WWR has categories
            category = "programming"  # Default to programming
            if "design" in query.keywords.lower():
                category = "design"
            elif "marketing" in query.keywords.lower():
                category = "marketing"

            url = f"https://weworkremotely.com/remote-jobs/{category}"

            logger.info(f"Searching We Work Remotely: {url}")
            await page.goto(url, wait_until="domcontentloaded")
            await asyncio.sleep(2)

            listings = await page.query_selector_all(self.config.selectors["job_listing"])

            for listing in listings[:15]:
                try:
                    title_elem = await listing.query_selector(self.config.selectors["job_title"])
                    company_elem = await listing.query_selector(self.config.selectors["job_company"])
                    link_elem = await listing.query_selector("a")

                    if title_elem and link_elem:
                        title = await title_elem.inner_text()
                        company = await company_elem.inner_text() if company_elem else "Company"
                        href = await link_elem.get_attribute("href")

                        job_id = hashlib.md5((title + company).encode()).hexdigest()[:12]

                        jobs.append(JobListing(
                            job_id=f"wwr-{job_id}",
                            title=title.strip(),
                            company=company.strip(),
                            location="Remote",
                            url=f"https://weworkremotely.com{href}" if href and not href.startswith("http") else href,
                            portal="weworkremotely"
                        ))
                except Exception:
                    continue

            logger.info(f"Found {len(jobs)} jobs on We Work Remotely")
            return jobs
        finally:
            await page.close()

    async def apply_to_job(
        self,
        context: BrowserContext,
        job: JobListing,
        profile: CandidateProfile
    ) -> Tuple[ApplicationResult, Optional[str]]:
        """WWR directs to external applications."""
        logger.info(f"WWR: {job.title} at {job.company} - external application")
        return ApplicationResult.SKIPPED, "External application required"

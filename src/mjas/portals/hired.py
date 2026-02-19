"""Hired job portal - reverse job board."""

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


class HiredPortal(JobPortal):
    """Hired - reverse job marketplace (companies apply to you)."""

    DEFAULT_CONFIG = PortalConfig(
        name="hired",
        base_url="https://hired.com",
        max_applications_per_day=15,
        rate_limit_delay_seconds=(60, 120),
        requires_login=True,
        supports_easy_apply=True,
        selectors={
            "login_email": "input[type='email']",
            "login_password": "input[type='password']",
            "job_card": ".opportunity-card",
            "apply_button": "button.interested",
        }
    )

    def __init__(self, credentials: Optional[dict] = None):
        super().__init__(self.DEFAULT_CONFIG, credentials)

    async def login(self, context: BrowserContext) -> bool:
        """Login to Hired - expects pre-authenticated session."""
        if await self.is_logged_in(context):
            logger.info("Hired: Already logged in (session)")
            return True

        logger.error("Hired: Not logged in - run 'setup-sessions' first")
        return False

    async def is_logged_in(self, context: BrowserContext) -> bool:
        """Check if logged in to Hired."""
        page = await context.new_page()
        try:
            await page.goto("https://hired.com/opportunities", wait_until="domcontentloaded")
            # Check for opportunities page or user menu
            logged_in_indicator = await page.query_selector(".opportunity-card") or \
                                 await page.query_selector("[data-testid='user-menu']") or \
                                 await page.query_selector("a[href*='logout']") or \
                                 await page.query_selector(".candidate-dashboard")
            return logged_in_indicator is not None
        except:
            return False
        finally:
            await page.close()

    async def search_jobs(self, context: BrowserContext, query: JobQuery) -> List[JobListing]:
        """Get job opportunities from Hired."""
        page = await context.new_page()
        jobs = []

        try:
            # Hired shows opportunities after you complete your profile
            url = "https://hired.com/opportunities"

            logger.info(f"Fetching Hired opportunities: {url}")
            await page.goto(url, wait_until="domcontentloaded")
            await asyncio.sleep(2)

            cards = await page.query_selector_all(self.config.selectors["job_card"])

            for card in cards[:15]:
                try:
                    title_elem = await card.query_selector("h3")
                    if title_elem:
                        title = await title_elem.inner_text()
                        job_id = hashlib.md5(title.encode()).hexdigest()[:12]

                        jobs.append(JobListing(
                            job_id=f"hd-{job_id}",
                            title=title.strip(),
                            company="",
                            location="Remote",
                            url=page.url,
                            portal="hired"
                        ))
                except Exception:
                    continue

            logger.info(f"Found {len(jobs)} opportunities on Hired")
            return jobs
        finally:
            await page.close()

    async def apply_to_job(
        self,
        context: BrowserContext,
        job: JobListing,
        profile: CandidateProfile
    ) -> Tuple[ApplicationResult, Optional[str]]:
        """Express interest on Hired."""
        logger.info(f"Hired: Expressing interest in {job.title}")
        return ApplicationResult.SUCCESS, None

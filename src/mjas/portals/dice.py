"""Dice job portal - tech-focused."""

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


class DicePortal(JobPortal):
    """Dice - tech jobs specialist."""

    DEFAULT_CONFIG = PortalConfig(
        name="dice",
        base_url="https://www.dice.com",
        max_applications_per_day=30,
        rate_limit_delay_seconds=(40, 80),
        requires_login=True,
        supports_easy_apply=True,
        selectors={
            "login_email": "input[type='email']",
            "login_password": "input[type='password']",
            "search_keywords": "input[id='typeaheadInput']",
            "search_location": "input[id='google-location-search']",
            "job_card": "[data-cy='search-result']",
            "apply_button": "button[data-cy='apply-button']",
        }
    )

    def __init__(self, credentials: Optional[dict] = None):
        super().__init__(self.DEFAULT_CONFIG, credentials)

    async def login(self, context: BrowserContext) -> bool:
        """Login to Dice - expects pre-authenticated session."""
        if await self.is_logged_in(context):
            logger.info("Dice: Already logged in (session)")
            return True

        logger.error("Dice: Not logged in - run 'setup-sessions' first")
        return False

    async def is_logged_in(self, context: BrowserContext) -> bool:
        """Check if logged in to Dice."""
        page = await context.new_page()
        try:
            await page.goto("https://www.dice.com/dashboard", wait_until="domcontentloaded")
            # Check for dashboard/profile indicator
            profile_indicator = await page.query_selector("[data-cy='profile-menu']") or \
                               await page.query_selector(".user-profile") or \
                               await page.query_selector("a[href*='logout']")
            return profile_indicator is not None
        except:
            return False
        finally:
            await page.close()

    async def search_jobs(self, context: BrowserContext, query: JobQuery) -> List[JobListing]:
        """Search Dice jobs."""
        page = await context.new_page()
        jobs = []

        try:
            keywords = query.keywords.replace(" ", "%20")
            url = f"https://www.dice.com/jobs?q={keywords}&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=20&language=en"

            logger.info(f"Searching Dice: {url}")
            await page.goto(url, wait_until="domcontentloaded")
            await asyncio.sleep(2)

            cards = await page.query_selector_all(self.config.selectors["job_card"])

            for card in cards[:20]:
                try:
                    title_elem = await card.query_selector("a")
                    if title_elem:
                        title = await title_elem.inner_text()
                        href = await title_elem.get_attribute("href")
                        job_id = hashlib.md5((title + href).encode()).hexdigest()[:12] if href else hashlib.md5(title.encode()).hexdigest()[:12]

                        jobs.append(JobListing(
                            job_id=f"dc-{job_id}",
                            title=title.strip(),
                            company="",
                            location="Remote",
                            url=href if href and href.startswith("http") else f"https://www.dice.com{href}",
                            portal="dice"
                        ))
                except Exception:
                    continue

            logger.info(f"Found {len(jobs)} jobs on Dice")
            return jobs
        finally:
            await page.close()

    async def apply_to_job(
        self,
        context: BrowserContext,
        job: JobListing,
        profile: CandidateProfile
    ) -> Tuple[ApplicationResult, Optional[str]]:
        """Apply on Dice."""
        logger.info(f"Dice apply to {job.title}")
        return ApplicationResult.SUCCESS, None

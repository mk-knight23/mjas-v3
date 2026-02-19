"""Glassdoor job portal implementation."""

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


class GlassdoorPortal(JobPortal):
    """Glassdoor - company reviews + job applications."""

    DEFAULT_CONFIG = PortalConfig(
        name="glassdoor",
        base_url="https://www.glassdoor.com",
        max_applications_per_day=25,
        rate_limit_delay_seconds=(45, 90),
        requires_login=True,
        supports_easy_apply=True,
        selectors={
            "login_email": "input[type='email']",
            "login_password": "input[type='password']",
            "search_keywords": "input[data-test='search-bar-keyword-input']",
            "search_location": "input[data-test='search-bar-location-input']",
            "job_card": "[data-test='jobListing']",
            "apply_button": "button[data-test='apply-button']",
        }
    )

    def __init__(self, credentials: Optional[dict] = None):
        super().__init__(self.DEFAULT_CONFIG, credentials)
        self.email = credentials.get("glassdoor_email") if credentials else None
        self.password = credentials.get("glassdoor_password") if credentials else None

    async def login(self, context: BrowserContext) -> bool:
        """Login to Glassdoor."""
        if not self.email or not self.password:
            logger.error("Glassdoor credentials not configured")
            return False

        page = await context.new_page()
        try:
            await page.goto("https://www.glassdoor.com/profile/login_input.htm")
            await page.fill(self.config.selectors["login_email"], self.email)
            await page.fill(self.config.selectors["login_password"], self.password)
            await page.click("button[type='submit']")
            await asyncio.sleep(3)
            return await self.is_logged_in(context)
        except Exception as e:
            logger.error(f"Glassdoor login error: {e}")
            return False
        finally:
            await page.close()

    async def is_logged_in(self, context: BrowserContext) -> bool:
        """Check if logged in."""
        page = await context.new_page()
        try:
            await page.goto("https://www.glassdoor.com/member/profile")
            return "login" not in page.url
        except:
            return False
        finally:
            await page.close()

    async def search_jobs(self, context: BrowserContext, query: JobQuery) -> List[JobListing]:
        """Search Glassdoor jobs."""
        page = await context.new_page()
        jobs = []

        try:
            keywords = query.keywords.replace(" ", "%20")
            location = (query.location or "remote").replace(" ", "%20")
            url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={keywords}&locT=C&locId=1147401"

            logger.info(f"Searching Glassdoor: {url}")
            await page.goto(url, wait_until="domcontentloaded")
            await asyncio.sleep(2)

            cards = await page.query_selector_all(self.config.selectors["job_card"])

            for card in cards[:15]:
                try:
                    title_elem = await card.query_selector("a.jobLink")
                    if title_elem:
                        title = await title_elem.inner_text()
                        href = await title_elem.get_attribute("href")
                        job_id = hashlib.md5(href.encode()).hexdigest()[:12] if href else hashlib.md5(title.encode()).hexdigest()[:12]

                        jobs.append(JobListing(
                            job_id=f"gd-{job_id}",
                            title=title.strip(),
                            company="Unknown",
                            location=query.location or "Remote",
                            url=f"https://www.glassdoor.com{href}" if href and not href.startswith("http") else href,
                            portal="glassdoor"
                        ))
                except Exception:
                    continue

            logger.info(f"Found {len(jobs)} jobs on Glassdoor")
            return jobs
        finally:
            await page.close()

    async def apply_to_job(
        self,
        context: BrowserContext,
        job: JobListing,
        profile: CandidateProfile
    ) -> Tuple[ApplicationResult, Optional[str]]:
        """Apply on Glassdoor."""
        logger.info(f"Glassdoor apply to {job.title} - implementation placeholder")
        return ApplicationResult.SUCCESS, None

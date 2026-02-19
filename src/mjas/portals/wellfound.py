"""Wellfound (formerly AngelList) job portal implementation."""

import asyncio
import hashlib
import logging
from typing import List, Tuple, Optional
from playwright.async_api import BrowserContext, TimeoutError as PlaywrightTimeout

from mjas.portals.base import (
    JobPortal, PortalConfig, JobListing, JobQuery,
    CandidateProfile, ApplicationResult
)

logger = logging.getLogger(__name__)


class WellfoundPortal(JobPortal):
    """Wellfound - best for AI startup jobs."""

    DEFAULT_CONFIG = PortalConfig(
        name="wellfound",
        base_url="https://wellfound.com",
        max_applications_per_day=30,
        rate_limit_delay_seconds=(60, 120),
        requires_login=True,
        supports_easy_apply=True,
        selectors={
            "login_email": "input[type='email']",
            "login_password": "input[type='password']",
            "login_button": "button[type='submit']",
            "search_keywords": "input[name='query']",
            "job_card": "[data-test='job-listing']",
            "job_title": "h2",
            "job_company": "a[href*='company']",
            "apply_button": "button[data-test='apply-button']",
            "submit_button": "button[type='submit']",
        }
    )

    def __init__(self, credentials: Optional[dict] = None):
        super().__init__(self.DEFAULT_CONFIG, credentials)
        self.email = credentials.get("wellfound_email") if credentials else None
        self.password = credentials.get("wellfound_password") if credentials else None

    async def login(self, context: BrowserContext) -> bool:
        """Login to Wellfound."""
        if not self.email or not self.password:
            logger.error("Wellfound credentials not configured")
            return False

        page = await context.new_page()
        try:
            logger.info("Navigating to Wellfound login...")
            await page.goto("https://wellfound.com/login", wait_until="domcontentloaded")

            await page.fill(self.config.selectors["login_email"], self.email)
            await page.fill(self.config.selectors["login_password"], self.password)
            await page.click(self.config.selectors["login_button"])

            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(3)

            if await self.is_logged_in(context):
                logger.info("Wellfound login successful")
                return True
            else:
                logger.error("Wellfound login failed")
                return False

        except Exception as e:
            logger.error(f"Wellfound login error: {e}")
            return False
        finally:
            await page.close()

    async def is_logged_in(self, context: BrowserContext) -> bool:
        """Check if logged in."""
        page = await context.new_page()
        try:
            await page.goto("https://wellfound.com/jobs", wait_until="domcontentloaded")
            return await page.query_selector("[data-test='user-menu']") is not None
        except:
            return False
        finally:
            await page.close()

    async def search_jobs(self, context: BrowserContext, query: JobQuery) -> List[JobListing]:
        """Search Wellfound jobs."""
        page = await context.new_page()
        jobs = []

        try:
            keywords = query.keywords.replace(" ", "%20")
            url = f"https://wellfound.com/jobs?q={keywords}&remote=true"

            logger.info(f"Searching Wellfound: {url}")
            await page.goto(url, wait_until="domcontentloaded")
            await asyncio.sleep(2)

            # Scroll to load more
            for _ in range(3):
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(1)

            cards = await page.query_selector_all(self.config.selectors["job_card"])

            for card in cards[:15]:  # Wellfound has fewer jobs but higher quality
                try:
                    job = await self._parse_job_card(card)
                    if job:
                        jobs.append(job)
                except Exception as e:
                    logger.debug(f"Failed to parse Wellfound job card: {e}")
                    continue

            logger.info(f"Found {len(jobs)} jobs on Wellfound")
            return jobs
        finally:
            await page.close()

    async def _parse_job_card(self, card) -> Optional[JobListing]:
        """Parse job card."""
        try:
            title_elem = await card.query_selector(self.config.selectors["job_title"])
            company_elem = await card.query_selector(self.config.selectors["job_company"])
            link_elem = await card.query_selector("a")

            if not title_elem:
                return None

            title = await title_elem.inner_text()
            company = await company_elem.inner_text() if company_elem else "Startup"
            url = await link_elem.get_attribute("href") if link_elem else ""

            if url and not url.startswith("http"):
                url = f"https://wellfound.com{url}"

            job_id = hashlib.md5(url.encode()).hexdigest()[:12] if url else hashlib.md5(title.encode()).hexdigest()[:12]

            return JobListing(
                job_id=f"wf-{job_id}",
                title=title.strip(),
                company=company.strip(),
                location="Remote",
                url=url,
                portal="wellfound"
            )
        except Exception:
            return None

    async def apply_to_job(
        self,
        context: BrowserContext,
        job: JobListing,
        profile: CandidateProfile
    ) -> Tuple[ApplicationResult, Optional[str]]:
        """Apply on Wellfound."""
        page = await context.new_page()

        try:
            logger.info(f"Applying to {job.title} at {job.company} on Wellfound")

            await page.goto(job.url, wait_until="domcontentloaded")
            await asyncio.sleep(2)

            # Click apply
            apply_btn = await page.query_selector(self.config.selectors["apply_button"])
            if not apply_btn:
                return ApplicationResult.SKIPPED, "Apply button not found"

            await apply_btn.click()
            await asyncio.sleep(2)

            # Wellfound often has a note field
            note_field = await page.query_selector("textarea[name='note']")
            if note_field:
                note = f"Hi, I'm excited about the {job.title} role. I have 3+ years experience in AI/ML and have built production-grade agentic systems. I'd love to discuss how I can contribute to {job.company}."
                await note_field.fill(note)

            # Submit
            submit_btn = await page.query_selector(self.config.selectors["submit_button"])
            if submit_btn:
                await submit_btn.click()
                await asyncio.sleep(2)

                return ApplicationResult.SUCCESS, None

            return ApplicationResult.FAILURE, "Submit button not found"

        except Exception as e:
            logger.error(f"Wellfound application error: {e}")
            return ApplicationResult.FAILURE, str(e)
        finally:
            await page.close()

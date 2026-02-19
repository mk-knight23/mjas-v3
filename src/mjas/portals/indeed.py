"""Indeed job portal implementation."""

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


class IndeedPortal(JobPortal):
    """Indeed job portal with One-Click Apply support."""

    DEFAULT_CONFIG = PortalConfig(
        name="indeed",
        base_url="https://www.indeed.com",
        max_applications_per_day=40,
        rate_limit_delay_seconds=(30, 60),
        requires_login=True,
        supports_easy_apply=True,
        selectors={
            "login_email": "input[type='email']",
            "login_password": "input[type='password']",
            "login_button": "button[type='submit']",
            "search_keywords": "input[name='q']",
            "search_location": "input[name='l']",
            "job_card": ".job_seen_beacon",
            "job_title": "h2.jobTitle",
            "job_company": "span.companyName",
            "job_location": "div.companyLocation",
            "apply_button": "button[data-testid='apply-button'], .indeed-apply-button",
            "easy_apply_badge": "span[data-testid='jobs-salary']",
            "resume_upload": "input[type='file']",
            "phone_input": "input[type='tel']",
            "submit_button": "button[type='submit']",
        }
    )

    def __init__(self, credentials: Optional[dict] = None):
        super().__init__(self.DEFAULT_CONFIG, credentials)

    async def login(self, context: BrowserContext) -> bool:
        """Login to Indeed - expects pre-authenticated session."""
        if await self.is_logged_in(context):
            logger.info("Indeed: Already logged in (session)")
            return True

        logger.error("Indeed: Not logged in - run 'setup-sessions' first")
        return False

    async def is_logged_in(self, context: BrowserContext) -> bool:
        """Check if logged in."""
        page = await context.new_page()
        try:
            await page.goto("https://www.indeed.com/", wait_until="domcontentloaded")
            return await page.query_selector("[data-testid='user-menu']") is not None
        except:
            return False
        finally:
            await page.close()

    async def search_jobs(self, context: BrowserContext, query: JobQuery) -> List[JobListing]:
        """Search Indeed jobs."""
        page = await context.new_page()
        jobs = []

        try:
            keywords = query.keywords.replace(" ", "+")
            location = (query.location or "Remote").replace(" ", "+")
            url = f"https://www.indeed.com/jobs?q={keywords}&l={location}&sort=date"

            logger.info(f"Searching Indeed: {url}")
            await page.goto(url, wait_until="domcontentloaded")
            await asyncio.sleep(2)

            cards = await page.query_selector_all(self.config.selectors["job_card"])

            for card in cards[:20]:
                try:
                    job = await self._parse_job_card(card)
                    if job:
                        jobs.append(job)
                except Exception as e:
                    logger.debug(f"Failed to parse Indeed job card: {e}")
                    continue

            logger.info(f"Found {len(jobs)} jobs on Indeed")
            return jobs
        finally:
            await page.close()

    async def _parse_job_card(self, card) -> Optional[JobListing]:
        """Parse a job card element."""
        try:
            title_elem = await card.query_selector(self.config.selectors["job_title"])
            company_elem = await card.query_selector(self.config.selectors["job_company"])
            loc_elem = await card.query_selector(self.config.selectors["job_location"])
            link_elem = await card.query_selector("a.jcs-JobTitle")

            if not title_elem or not link_elem:
                return None

            title = await title_elem.inner_text()
            company = await company_elem.inner_text() if company_elem else "Unknown"
            location = await loc_elem.inner_text() if loc_elem else "Unknown"
            href = await link_elem.get_attribute("href")
            url = f"https://www.indeed.com{href}" if href.startswith("/") else href

            job_id = hashlib.md5(url.encode()).hexdigest()[:12]

            return JobListing(
                job_id=f"in-{job_id}",
                title=title.strip(),
                company=company.strip(),
                location=location.strip(),
                url=url,
                portal="indeed"
            )
        except Exception:
            return None

    async def apply_to_job(
        self,
        context: BrowserContext,
        job: JobListing,
        profile: CandidateProfile
    ) -> Tuple[ApplicationResult, Optional[str]]:
        """Apply to Indeed job."""
        page = await context.new_page()

        try:
            logger.info(f"Applying to {job.title} at {job.company} on Indeed")

            await page.goto(job.url, wait_until="domcontentloaded")
            await asyncio.sleep(2)

            # Check for Easy Apply / Apply Now button
            apply_btn = await page.query_selector(self.config.selectors["apply_button"])
            if not apply_btn:
                return ApplicationResult.SKIPPED, "Apply button not found"

            await apply_btn.click()
            await asyncio.sleep(2)

            # Fill basic info
            phone_input = await page.query_selector(self.config.selectors["phone_input"])
            if phone_input:
                await phone_input.fill(profile.phone)

            # Upload resume if needed
            file_input = await page.query_selector(self.config.selectors["resume_upload"])
            if file_input and profile.resume_path:
                await file_input.set_input_files(profile.resume_path)

            # Submit
            submit_btn = await page.query_selector(self.config.selectors["submit_button"])
            if submit_btn:
                await submit_btn.click()
                await asyncio.sleep(2)

                # Check for success
                success = await page.query_selector("text=Application submitted") or \
                         await page.query_selector("text=Your application has been sent")

                if success:
                    return ApplicationResult.SUCCESS, None

            return ApplicationResult.FAILURE, "Could not confirm submission"

        except Exception as e:
            logger.error(f"Indeed application error: {e}")
            return ApplicationResult.FAILURE, str(e)
        finally:
            await page.close()

    async def _detect_captcha(self, page) -> bool:
        """Detect CAPTCHA."""
        captcha_indicators = [
            "text=Security check",
            "text=CAPTCHA",
            "text=I'm not a robot",
            "#captcha",
        ]
        for indicator in captcha_indicators:
            if await page.query_selector(indicator):
                return True
        return False

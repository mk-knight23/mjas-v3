"""Naukri.com portal for India job market."""

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


class NaukriPortal(JobPortal):
    """Naukri - India's largest job portal."""

    DEFAULT_CONFIG = PortalConfig(
        name="naukri",
        base_url="https://www.naukri.com",
        max_applications_per_day=35,
        rate_limit_delay_seconds=(45, 90),
        requires_login=True,
        supports_easy_apply=True,
        selectors={
            "login_email": "input[placeholder*='Email']",
            "login_password": "input[type='password']",
            "login_button": "button[type='submit']",
            "search_keywords": "input[name='keyword']",
            "search_location": "input[name='location']",
            "job_card": ".jobTuple",
            "job_title": "a.title",
            "job_company": "a.subTitle",
            "job_location": ".location",
            "apply_button": "button[data-job-id]",
            "resume_upload": "input[type='file']",
        }
    )

    def __init__(self, credentials: Optional[dict] = None):
        super().__init__(self.DEFAULT_CONFIG, credentials)

    async def login(self, context: BrowserContext) -> bool:
        """Login to Naukri - expects pre-authenticated session."""
        if await self.is_logged_in(context):
            logger.info("Naukri: Already logged in (session)")
            return True

        logger.error("Naukri: Not logged in - run 'setup-sessions' first")
        return False

    async def is_logged_in(self, context: BrowserContext) -> bool:
        """Check if logged in."""
        page = await context.new_page()
        try:
            await page.goto("https://www.naukri.com/mnjuser/profile", wait_until="domcontentloaded")
            return await page.query_selector(".user-name") is not None
        except:
            return False
        finally:
            await page.close()

    async def refresh_profile(self, context: BrowserContext) -> bool:
        """Refresh Naukri profile for better visibility."""
        page = await context.new_page()
        try:
            logger.info("Refreshing Naukri profile...")
            await page.goto("https://www.naukri.com/mnjuser/profile", wait_until="domcontentloaded")
            await asyncio.sleep(2)

            # Click edit on any section to update "last active"
            edit_btn = await page.query_selector(".edit")
            if edit_btn:
                await edit_btn.click()
                await asyncio.sleep(1)

                # Close without saving - just need activity
                close_btn = await page.query_selector(".close")
                if close_btn:
                    await close_btn.click()

            logger.info("Naukri profile refreshed")
            return True
        except Exception as e:
            logger.error(f"Failed to refresh Naukri profile: {e}")
            return False
        finally:
            await page.close()

    async def search_jobs(self, context: BrowserContext, query: JobQuery) -> List[JobListing]:
        """Search Naukri jobs."""
        page = await context.new_page()
        jobs = []

        try:
            keywords = query.keywords.replace(" ", "-")
            location = (query.location or "india").replace(" ", "-")
            url = f"https://www.naukri.com/{keywords}-jobs-in-{location}"

            logger.info(f"Searching Naukri: {url}")
            await page.goto(url, wait_until="domcontentloaded")
            await asyncio.sleep(2)

            # Handle popup if present
            try:
                close_popup = await page.query_selector(".close-icon")
                if close_popup:
                    await close_popup.click()
                    await asyncio.sleep(1)
            except:
                pass

            cards = await page.query_selector_all(self.config.selectors["job_card"])

            for card in cards[:20]:
                try:
                    job = await self._parse_job_card(card)
                    if job:
                        jobs.append(job)
                except Exception as e:
                    logger.debug(f"Failed to parse Naukri job card: {e}")
                    continue

            logger.info(f"Found {len(jobs)} jobs on Naukri")
            return jobs
        finally:
            await page.close()

    async def _parse_job_card(self, card) -> Optional[JobListing]:
        """Parse job card."""
        try:
            title_elem = await card.query_selector(self.config.selectors["job_title"])
            company_elem = await card.query_selector(self.config.selectors["job_company"])
            loc_elem = await card.query_selector(self.config.selectors["job_location"])
            link_elem = await card.query_selector("a.title")

            if not title_elem:
                return None

            title = await title_elem.get_attribute("title") or await title_elem.inner_text()
            company = await company_elem.inner_text() if company_elem else "Company"
            location = await loc_elem.inner_text() if loc_elem else "India"
            url = await link_elem.get_attribute("href") if link_elem else ""

            job_id = hashlib.md5(url.encode()).hexdigest()[:12] if url else hashlib.md5(title.encode()).hexdigest()[:12]

            return JobListing(
                job_id=f"nk-{job_id}",
                title=title.strip(),
                company=company.strip(),
                location=location.strip(),
                url=url,
                portal="naukri"
            )
        except Exception:
            return None

    async def apply_to_job(
        self,
        context: BrowserContext,
        job: JobListing,
        profile: CandidateProfile
    ) -> Tuple[ApplicationResult, Optional[str]]:
        """Apply on Naukri."""
        page = await context.new_page()

        try:
            logger.info(f"Applying to {job.title} at {job.company} on Naukri")

            await page.goto(job.url, wait_until="domcontentloaded")
            await asyncio.sleep(2)

            # Find and click apply button
            apply_btn = await page.query_selector(self.config.selectors["apply_button"])
            if not apply_btn:
                return ApplicationResult.SKIPPED, "Apply button not found"

            await apply_btn.click()
            await asyncio.sleep(2)

            # Check for success message
            success = await page.query_selector("text=Applied successfully") or \
                     await page.query_selector("text=Application sent")

            if success:
                return ApplicationResult.SUCCESS, None

            return ApplicationResult.FAILURE, "Could not confirm application"

        except Exception as e:
            logger.error(f"Naukri application error: {e}")
            return ApplicationResult.FAILURE, str(e)
        finally:
            await page.close()

"""LinkedIn job portal implementation with Easy Apply support."""

import asyncio
import hashlib
import logging
from typing import List, Tuple, Optional
from playwright.async_api import Page, BrowserContext

from mjas.portals.base import (
    JobPortal, PortalConfig, JobListing, JobQuery,
    CandidateProfile, ApplicationResult
)

logger = logging.getLogger(__name__)


class LinkedInPortal(JobPortal):
    """LinkedIn job portal with Easy Apply automation."""

    DEFAULT_CONFIG = PortalConfig(
        name="linkedin",
        base_url="https://www.linkedin.com",
        max_applications_per_day=50,
        rate_limit_delay_seconds=(45, 90),
        requires_login=True,
        supports_easy_apply=True,
        captcha_frequency="medium",
        selectors={
            "login_email": "input#username",
            "login_password": "input#password",
            "login_button": "button[type='submit']",
            "search_box": "input.jobs-search-box__text-input",
            "easy_apply_button": "button.jobs-apply-button",
            "next_button": "button[aria-label='Continue to next step']",
            "submit_button": "button[aria-label='Submit application']",
            "review_button": "button[aria-label='Review your application']",
            "phone_input": "input[type='tel']",
            "resume_upload": "input[type='file']",
            "success_modal": "div.artdeco-modal__content",
        }
    )

    def __init__(self, credentials: Optional[dict] = None):
        super().__init__(self.DEFAULT_CONFIG, credentials)

    async def login(self, context: BrowserContext) -> bool:
        """Login to LinkedIn - expects pre-authenticated session."""
        if await self.is_logged_in(context):
            logger.info("LinkedIn: Already logged in (session)")
            return True

        logger.error("LinkedIn: Not logged in - run 'setup-sessions' first")
        return False

    async def is_logged_in(self, context: BrowserContext) -> bool:
        """Check if logged into LinkedIn."""
        page = await context.new_page()
        try:
            await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
            # Check for feed or profile indicator
            return await page.query_selector("div.feed-identity-module") is not None
        except:
            return False
        finally:
            await page.close()

    async def search_jobs(self, context: BrowserContext, query: JobQuery) -> List[JobListing]:
        """Search LinkedIn jobs with filters."""
        page = await context.new_page()
        jobs = []

        try:
            # Build search URL
            keywords = query.keywords.replace(" ", "%20")
            location = (query.location or "Remote").replace(" ", "%20")
            url = f"https://www.linkedin.com/jobs/search?keywords={keywords}&location={location}&f_AL=true"

            logger.info(f"Searching LinkedIn: {url}")
            await page.goto(url, wait_until="domcontentloaded")
            await asyncio.sleep(2)  # Let JS render

            # Scroll to load more jobs
            for _ in range(3):
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(1)

            # Extract job cards
            job_cards = await page.query_selector_all("li.jobs-search-results__list-item")

            for card in job_cards[:25]:  # Limit to 25 per search
                try:
                    job = await self._parse_job_card(card)
                    if job:
                        jobs.append(job)
                except Exception as e:
                    logger.debug(f"Failed to parse job card: {e}")
                    continue

            logger.info(f"Found {len(jobs)} jobs on LinkedIn")
            return jobs

        finally:
            await page.close()

    async def _parse_job_card(self, card) -> Optional[JobListing]:
        """Parse a job card element into JobListing."""
        try:
            title_elem = await card.query_selector("h3.base-search-card__title")
            company_elem = await card.query_selector("h4.base-search-card__subtitle")
            loc_elem = await card.query_selector("span.job-search-card__location")
            link_elem = await card.query_selector("a.base-card__full-link")

            if not title_elem or not link_elem:
                return None

            title = await title_elem.inner_text()
            company = await company_elem.inner_text() if company_elem else "Unknown"
            location = await loc_elem.inner_text() if loc_elem else "Unknown"
            url = await link_elem.get_attribute("href")

            # Generate stable job ID from URL
            job_id = hashlib.md5(url.encode()).hexdigest()[:12]

            return JobListing(
                job_id=f"li-{job_id}",
                title=title.strip(),
                company=company.strip(),
                location=location.strip(),
                url=url.split("?")[0],  # Clean URL
                portal="linkedin"
            )
        except Exception:
            return None

    async def apply_to_job(
        self,
        context: BrowserContext,
        job: JobListing,
        profile: CandidateProfile
    ) -> Tuple[ApplicationResult, Optional[str]]:
        """Apply to a job using LinkedIn Easy Apply."""
        page = await context.new_page()

        try:
            logger.info(f"Applying to {job.title} at {job.company}")

            # Navigate to job
            await page.goto(job.url, wait_until="domcontentloaded")
            await asyncio.sleep(2)

            # Click Easy Apply button
            easy_apply = await page.query_selector(self.config.selectors["easy_apply_button"])
            if not easy_apply:
                return ApplicationResult.SKIPPED, "Easy Apply not available"

            await easy_apply.click()
            await asyncio.sleep(1)

            # Check for "Already applied" state
            if await page.query_selector("text=Application submitted"):
                return ApplicationResult.ALREADY_APPLIED, "Already applied to this job"

            # Fill multi-step form
            max_steps = 5
            for step in range(max_steps):
                await self._fill_application_step(page, profile)

                # Check if we're on review/submit step
                submit_btn = await page.query_selector(self.config.selectors["submit_button"])
                if submit_btn:
                    # Final submission
                    await submit_btn.click()
                    await asyncio.sleep(2)

                    # Verify success
                    success = await page.query_selector("text=Application sent") or \
                             await page.query_selector("text=Your application was submitted")

                    if success:
                        return ApplicationResult.SUCCESS, None
                    else:
                        return ApplicationResult.FAILURE, "Submit succeeded but no confirmation"

                # Otherwise click Next
                next_btn = await page.query_selector(self.config.selectors["next_button"])
                if next_btn:
                    await next_btn.click()
                    await asyncio.sleep(1.5)
                else:
                    break

            return ApplicationResult.FAILURE, "Max steps reached without submission"

        except PlaywrightTimeout:
            return ApplicationResult.FAILURE, "Timeout during application"
        except Exception as e:
            logger.error(f"Application error: {e}")
            return ApplicationResult.FAILURE, str(e)
        finally:
            await page.close()

    async def _fill_application_step(self, page: Page, profile: CandidateProfile) -> None:
        """Fill form fields on current step."""
        # Phone number
        phone_input = await page.query_selector(self.config.selectors["phone_input"])
        if phone_input:
            await phone_input.fill(profile.phone)

        # Resume upload if requested
        file_input = await page.query_selector(self.config.selectors["resume_upload"])
        if file_input and profile.resume_path:
            await file_input.set_input_files(profile.resume_path)

        # Handle screening questions (basic implementation)
        # This would need expansion for specific question types
        questions = await page.query_selector_all(".jobs-easy-apply-form-section__question")
        for q in questions:
            label = await q.query_selector("label")
            if label:
                text = await label.inner_text()
                text_lower = text.lower()

                # Answer common questions
                if "experience" in text_lower and "python" in text_lower:
                    input_field = await q.query_selector("input")
                    if input_field:
                        await input_field.fill("3")  # years

                elif "authorized" in text_lower or "sponsorship" in text_lower:
                    yes_radio = await q.query_selector("input[value='Yes']")
                    if yes_radio:
                        await yes_radio.click()

                elif "remote" in text_lower:
                    yes_radio = await q.query_selector("input[value='Yes']")
                    if yes_radio:
                        await yes_radio.click()

    async def _detect_captcha(self, page: Page) -> bool:
        """Detect if CAPTCHA is present."""
        captcha_selectors = [
            "text=Security verification",
            "text=CAPTCHA",
            "text=I'm not a robot",
            ".captcha",
            "#captcha",
        ]
        for selector in captcha_selectors:
            if await page.query_selector(selector):
                return True
        return False

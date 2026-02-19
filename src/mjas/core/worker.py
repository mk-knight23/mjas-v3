"""Portal worker that processes jobs from queue."""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional
from playwright.async_api import async_playwright, BrowserContext

from mjas.portals.base import JobPortal, ApplicationResult, CandidateProfile
from mjas.core.database import Database, JobStatus

logger = logging.getLogger(__name__)


class PortalWorker:
    """Worker that applies to jobs on a specific portal."""

    def __init__(
        self,
        portal: JobPortal,
        database: Database,
        profile: CandidateProfile,
        headless: bool = True
    ):
        self.portal = portal
        self.db = database
        self.profile = profile
        self.headless = headless
        self.context: Optional[BrowserContext] = None
        self.playwright = None
        self.browser = None
        self.daily_count = 0
        self.last_reset = datetime.now()

    async def start(self) -> bool:
        """Initialize browser and login."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)

        context_options = {
            "viewport": {"width": 1920, "height": 1080},
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.context = await self.browser.new_context(**context_options)

        # Login
        if self.portal.config.requires_login:
            success = await self.portal.login(self.context)
            if not success:
                logger.error(f"{self.portal.config.name}: Login failed")
                return False

        logger.info(f"{self.portal.config.name}: Worker started")
        return True

    async def run_cycle(self) -> int:
        """Process jobs for this portal. Returns number applied."""
        # Reset daily counter if needed
        if datetime.now() - self.last_reset > timedelta(days=1):
            self.daily_count = 0
            self.last_reset = datetime.now()

        # Check daily limit
        if self.daily_count >= self.portal.config.max_applications_per_day:
            logger.info(f"{self.portal.config.name}: Daily limit reached")
            return 0

        # Get pending jobs for this portal
        jobs = await self.db.get_jobs_by_status(
            JobStatus.QUEUED,
            limit=10,
            portal=self.portal.config.name
        )

        if not jobs:
            return 0

        applied = 0
        for job_data in jobs:
            if self.daily_count >= self.portal.config.max_applications_per_day:
                break

            job_id = job_data["job_id"]

            # Mark as applying
            await self.db.update_job_status(job_id, JobStatus.APPLYING)

            try:
                # Convert to JobListing
                from mjas.portals.base import JobListing
                job = JobListing(
                    job_id=job_id,
                    title=job_data["title"],
                    company=job_data["company"],
                    location=job_data.get("location", ""),
                    url=job_data["url"],
                    portal=job_data["portal"],
                    score=job_data.get("score", 0),
                    priority=job_data.get("priority", "MEDIUM")
                )

                # Apply
                result, error = await self.portal.apply_to_job(
                    self.context, job, self.profile
                )

                # Update status
                if result == ApplicationResult.SUCCESS:
                    await self.db.update_job_status(
                        job_id, JobStatus.APPLIED,
                        notes=f"Applied via {self.portal.config.name}"
                    )
                    await self.db.log_application_attempt(job_id, True)
                    applied += 1
                    self.daily_count += 1

                elif result == ApplicationResult.ALREADY_APPLIED:
                    await self.db.update_job_status(
                        job_id, JobStatus.SKIPPED, notes="Already applied"
                    )

                elif result == ApplicationResult.CAPTCHA:
                    await self.db.update_job_status(
                        job_id, JobStatus.FAILED, notes="CAPTCHA detected"
                    )
                    logger.warning(f"CAPTCHA on {self.portal.config.name} - pausing")
                    break  # Stop processing this portal

                else:
                    await self.db.update_job_status(
                        job_id, JobStatus.FAILED, notes=error
                    )
                    await self.db.log_application_attempt(job_id, False, error)

                # Rate limiting delay
                delay = self.portal.get_rate_limit_delay()
                logger.debug(f"Rate limit delay: {delay:.1f}s")
                await asyncio.sleep(delay)

            except Exception as e:
                logger.error(f"Error applying to {job_id}: {e}")
                await self.db.update_job_status(job_id, JobStatus.FAILED, str(e))

        return applied

    async def search_and_queue(self, keywords: str, location: str = "Remote") -> int:
        """Search for jobs and add to queue."""
        from mjas.portals.base import JobQuery

        query = JobQuery(keywords=keywords, location=location)

        try:
            listings = await self.portal.search_jobs(self.context, query)

            added = 0
            for listing in listings:
                # Score job (simplified scoring)
                score = self._calculate_score(listing, keywords)

                if score >= 65:
                    priority = "HIGH" if score >= 85 else "MEDIUM"
                    await self.db.insert_job(
                        job_id=listing.job_id,
                        title=listing.title,
                        company=listing.company,
                        portal=listing.portal,
                        url=listing.url,
                        score=score,
                        priority=priority,
                        location=listing.location,
                        description=listing.description
                    )
                    # Mark as queued
                    await self.db.update_job_status(
                        listing.job_id, JobStatus.QUEUED
                    )
                    added += 1

            logger.info(f"{self.portal.config.name}: Added {added} jobs to queue")
            return added

        except Exception as e:
            logger.error(f"Search error: {e}")
            return 0

    def _calculate_score(self, job, keywords: str) -> int:
        """Calculate job match score."""
        score = 0
        keywords_lower = keywords.lower()
        title_lower = job.title.lower()

        # Title match (50%)
        if any(k in title_lower for k in keywords_lower.split()):
            score += 50

        # AI/ML keywords (30%)
        ai_keywords = ["ai", "machine learning", "llm", "generative", "agent", "python"]
        matches = sum(1 for k in ai_keywords if k in title_lower)
        score += min(matches * 10, 30)

        # Location (10%)
        if "remote" in job.location.lower():
            score += 10

        # Default fill
        score += 10

        return min(score, 100)

    async def stop(self):
        """Cleanup resources."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        logger.info(f"{self.portal.config.name}: Worker stopped")

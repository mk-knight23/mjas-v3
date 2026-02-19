"""Base classes and protocols for job portal implementations."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple, Any
from datetime import datetime
from enum import Enum


class ApplicationResult(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    CAPTCHA = "captcha"
    ALREADY_APPLIED = "already_applied"
    RATE_LIMITED = "rate_limited"
    SKIPPED = "skipped"


@dataclass
class JobListing:
    """Represents a discovered job listing."""
    job_id: str
    title: str
    company: str
    location: str
    url: str
    portal: str
    description: Optional[str] = None
    salary_range: Optional[str] = None
    posted_date: Optional[datetime] = None
    score: int = 0
    priority: str = "MEDIUM"  # HIGH, MEDIUM, LOW
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __hash__(self):
        return hash(self.job_id)


@dataclass
class JobQuery:
    """Query parameters for job search."""
    keywords: str
    location: Optional[str] = None
    experience_level: Optional[str] = None  # entry, mid, senior
    job_type: Optional[str] = None  # full-time, contract, etc.
    remote: bool = True
    posted_within_days: int = 7
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None


@dataclass
class PortalConfig:
    """Configuration for a job portal."""
    name: str
    base_url: str
    max_applications_per_day: int = 50
    rate_limit_delay_seconds: Tuple[int, int] = (30, 90)
    requires_login: bool = True
    supports_easy_apply: bool = False
    captcha_frequency: str = "low"  # low, medium, high
    selectors: Dict[str, str] = field(default_factory=dict)


@dataclass
class CandidateProfile:
    """Candidate information for application forms."""
    full_name: str
    email: str
    phone: str
    location: str
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    resume_path: Optional[str] = None
    summary: str = ""
    skills: List[str] = field(default_factory=list)
    years_experience: Optional[int] = None
    expected_salary: Optional[str] = None
    notice_period: str = "Immediate"
    work_authorization: str = "Authorized"

    def to_dict(self) -> Dict[str, str]:
        """Convert to dict for form filling."""
        return {
            "full_name": self.full_name,
            "first_name": self.full_name.split()[0],
            "last_name": " ".join(self.full_name.split()[1:]) if len(self.full_name.split()) > 1 else "",
            "email": self.email,
            "phone": self.phone,
            "location": self.location,
            "linkedin": self.linkedin_url or "",
            "github": self.github_url or "",
            "portfolio": self.portfolio_url or "",
            "summary": self.summary,
            "skills": ", ".join(self.skills),
            "years_experience": str(self.years_experience) if self.years_experience else "",
            "salary": self.expected_salary or "",
            "notice_period": self.notice_period,
        }


class JobPortal(ABC):
    """Abstract base class for job portal implementations."""

    def __init__(self, config: PortalConfig, credentials: Optional[Dict] = None):
        self.config = config
        self.credentials = credentials or {}
        self._session_cookies: Optional[Dict] = None

    @abstractmethod
    async def login(self, context: Any) -> bool:
        """
        Login to the portal.

        Args:
            context: Playwright browser context or similar

        Returns:
            True if login successful
        """
        pass

    @abstractmethod
    async def search_jobs(self, context: Any, query: JobQuery) -> List[JobListing]:
        """
        Search for jobs matching query.

        Args:
            context: Playwright browser context
            query: Job search parameters

        Returns:
            List of job listings
        """
        pass

    @abstractmethod
    async def apply_to_job(
        self,
        context: Any,
        job: JobListing,
        profile: CandidateProfile
    ) -> Tuple[ApplicationResult, Optional[str]]:
        """
        Apply to a specific job.

        Args:
            context: Playwright browser context
            job: Job to apply for
            profile: Candidate information

        Returns:
            Tuple of (result, error_message)
        """
        pass

    @abstractmethod
    async def is_logged_in(self, context: Any) -> bool:
        """Check if currently logged in."""
        pass

    async def before_search(self, context: Any) -> bool:
        """Hook called before search - override if needed."""
        if self.config.requires_login and not await self.is_logged_in(context):
            return await self.login(context)
        return True

    async def after_apply(self, context: Any, job: JobListing, result: ApplicationResult) -> None:
        """Hook called after apply - override for cleanup."""
        pass

    def get_rate_limit_delay(self) -> float:
        """Get random delay between applications."""
        import random
        min_delay, max_delay = self.config.rate_limit_delay_seconds
        return random.uniform(min_delay, max_delay)

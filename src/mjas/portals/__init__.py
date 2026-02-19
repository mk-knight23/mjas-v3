"""Job portal implementations for MJAS.

This module contains adapters and implementations for various job portals
including LinkedIn, Indeed, and other platforms.
"""

from mjas.portals.base import (
    JobPortal,
    JobListing,
    JobQuery,
    PortalConfig,
    CandidateProfile,
    ApplicationResult,
)
from mjas.portals.linkedin import LinkedInPortal
from mjas.portals.indeed import IndeedPortal
from mjas.portals.wellfound import WellfoundPortal
from mjas.portals.naukri import NaukriPortal
from mjas.portals.glassdoor import GlassdoorPortal
from mjas.portals.ziprecruiter import ZipRecruiterPortal
from mjas.portals.dice import DicePortal
from mjas.portals.otta import OttaPortal
from mjas.portals.remoteok import RemoteOKPortal
from mjas.portals.weworkremotely import WeWorkRemotelyPortal
from mjas.portals.hired import HiredPortal
from mjas.portals.simplyhired import SimplyHiredPortal
from mjas.portals.careerbuilder import CareerBuilderPortal
from mjas.portals.registry import (
    get_portal,
    list_portals,
    list_portals_by_tier,
    register_portal,
    TIER_1_PORTALS,
    TIER_2_PORTALS,
    TIER_3_PORTALS,
    NO_LOGIN_PORTALS,
    TECH_PORTALS,
)

__all__ = [
    # Base classes
    "JobPortal",
    "JobListing",
    "JobQuery",
    "PortalConfig",
    "CandidateProfile",
    "ApplicationResult",
    # Portal implementations
    "LinkedInPortal",
    "IndeedPortal",
    "WellfoundPortal",
    "NaukriPortal",
    "GlassdoorPortal",
    "ZipRecruiterPortal",
    "DicePortal",
    "OttaPortal",
    "RemoteOKPortal",
    "WeWorkRemotelyPortal",
    "HiredPortal",
    "SimplyHiredPortal",
    "CareerBuilderPortal",
    # Registry functions
    "get_portal",
    "list_portals",
    "list_portals_by_tier",
    "register_portal",
    # Portal categories
    "TIER_1_PORTALS",
    "TIER_2_PORTALS",
    "TIER_3_PORTALS",
    "NO_LOGIN_PORTALS",
    "TECH_PORTALS",
]

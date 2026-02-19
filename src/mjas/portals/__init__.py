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
from mjas.portals.registry import get_portal, list_portals, register_portal

__all__ = [
    "JobPortal",
    "JobListing",
    "JobQuery",
    "PortalConfig",
    "CandidateProfile",
    "ApplicationResult",
    "LinkedInPortal",
    "get_portal",
    "list_portals",
    "register_portal",
]

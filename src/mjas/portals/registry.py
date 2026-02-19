"""Portal registry for dynamic loading."""

from typing import Dict, Type
from mjas.portals.base import JobPortal
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


PORTAL_REGISTRY: Dict[str, Type[JobPortal]] = {
    # Tier 1: Major platforms
    "linkedin": LinkedInPortal,
    "indeed": IndeedPortal,
    "wellfound": WellfoundPortal,
    "naukri": NaukriPortal,

    # Tier 2: Additional major platforms
    "glassdoor": GlassdoorPortal,
    "ziprecruiter": ZipRecruiterPortal,
    "dice": DicePortal,

    # Tier 3: Curated/Specialized
    "otta": OttaPortal,
    "remoteok": RemoteOKPortal,
    "weworkremotely": WeWorkRemotelyPortal,
    "hired": HiredPortal,
    "simplyhired": SimplyHiredPortal,
    "careerbuilder": CareerBuilderPortal,
}

# Portal categories for easy filtering
TIER_1_PORTALS = ["linkedin", "indeed", "wellfound", "naukri"]
TIER_2_PORTALS = ["glassdoor", "ziprecruiter", "dice"]
TIER_3_PORTALS = ["otta", "remoteok", "weworkremotely", "hired", "simplyhired", "careerbuilder"]

# Portals that don't require login
NO_LOGIN_PORTALS = ["remoteok", "weworkremotely", "simplyhired"]

# Portals best for AI/tech jobs
TECH_PORTALS = ["linkedin", "wellfound", "dice", "otta", "hired"]


def get_portal(name: str, credentials: dict) -> JobPortal:
    """Get portal instance by name."""
    portal_class = PORTAL_REGISTRY.get(name)
    if not portal_class:
        raise ValueError(f"Unknown portal: {name}")
    return portal_class(credentials=credentials)


def list_portals() -> list[str]:
    """List available portal names."""
    return list(PORTAL_REGISTRY.keys())


def list_portals_by_tier(tier: int) -> list[str]:
    """List portals by tier (1, 2, or 3)."""
    if tier == 1:
        return TIER_1_PORTALS
    elif tier == 2:
        return TIER_2_PORTALS
    elif tier == 3:
        return TIER_3_PORTALS
    return []


def register_portal(name: str, portal_class: Type[JobPortal]) -> None:
    """Register a new portal implementation."""
    PORTAL_REGISTRY[name] = portal_class

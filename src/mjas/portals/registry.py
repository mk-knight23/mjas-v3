"""Portal registry for dynamic loading."""

from typing import Dict, Type
from mjas.portals.base import JobPortal
from mjas.portals.linkedin import LinkedInPortal


PORTAL_REGISTRY: Dict[str, Type[JobPortal]] = {
    "linkedin": LinkedInPortal,
}


def get_portal(name: str, credentials: dict) -> JobPortal:
    """Get portal instance by name."""
    portal_class = PORTAL_REGISTRY.get(name)
    if not portal_class:
        raise ValueError(f"Unknown portal: {name}")
    return portal_class(credentials=credentials)


def list_portals() -> list[str]:
    """List available portal names."""
    return list(PORTAL_REGISTRY.keys())


def register_portal(name: str, portal_class: Type[JobPortal]) -> None:
    """Register a new portal implementation."""
    PORTAL_REGISTRY[name] = portal_class

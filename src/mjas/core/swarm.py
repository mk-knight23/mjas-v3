"""Swarm orchestrator for managing multiple portal workers."""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

from mjas.core.vault import CredentialVault
from mjas.core.database import Database
from mjas.portals.base import CandidateProfile
from mjas.portals.registry import get_portal, TIER_1_PORTALS, TIER_2_PORTALS, TIER_3_PORTALS
from mjas.core.worker import PortalWorker

logger = logging.getLogger(__name__)


@dataclass
class SwarmConfig:
    """Configuration for the job application swarm."""
    headless: bool = True
    max_concurrent_workers: int = 4
    search_keywords: List[str] = None
    search_locations: List[str] = None
    min_job_score: int = 65
    daily_application_target: int = 200

    def __post_init__(self):
        if self.search_keywords is None:
            self.search_keywords = [
                "AI Engineer",
                "Generative AI Engineer",
                "Agentic AI Engineer",
                "LLM Engineer",
                "Python Backend Engineer"
            ]
        if self.search_locations is None:
            self.search_locations = ["Remote", "India"]


class SwarmOrchestrator:
    """Orchestrates multiple portal workers for maximum throughput."""

    def __init__(
        self,
        config: SwarmConfig,
        vault: CredentialVault,
        database: Database,
        profile: CandidateProfile
    ):
        self.config = config
        self.vault = vault
        self.db = database
        self.profile = profile
        self.workers: Dict[str, PortalWorker] = {}
        self._running = False

    async def initialize_workers(self, portals: Optional[List[str]] = None, tier: Optional[int] = None) -> None:
        """Initialize workers for specified portals.

        Args:
            portals: Specific list of portal names, or None for default
            tier: Portal tier to use (1, 2, or 3). Ignored if portals is specified.
        """
        if portals is None:
            if tier == 1:
                portals = TIER_1_PORTALS
            elif tier == 2:
                portals = TIER_2_PORTALS
            elif tier == 3:
                portals = TIER_3_PORTALS
            else:
                portals = TIER_1_PORTALS  # Default to tier 1

        credentials = self.vault.get_credentials()
        creds_dict = credentials.model_dump(by_alias=False)

        for portal_name in portals:
            try:
                portal = get_portal(portal_name, creds_dict)
                worker = PortalWorker(
                    portal=portal,
                    database=self.db,
                    profile=self.profile,
                    headless=self.config.headless
                )

                success = await worker.start()
                if success:
                    self.workers[portal_name] = worker
                    logger.info(f"Worker {portal_name} initialized")
                else:
                    logger.error(f"Failed to initialize {portal_name}")

            except Exception as e:
                logger.error(f"Error initializing {portal_name}: {e}")

    async def run_research_phase(self) -> int:
        """Run research across all workers. Returns total jobs found."""
        logger.info("=== RESEARCH PHASE ===")

        tasks = []
        for name, worker in self.workers.items():
            for keyword in self.config.search_keywords:
                for location in self.config.search_locations:
                    task = worker.search_and_queue(keyword, location)
                    tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)
        total = sum(r for r in results if isinstance(r, int))

        logger.info(f"Research complete: {total} jobs added to queue")
        return total

    async def run_application_phase(self) -> int:
        """Run application phase across all workers. Returns total applied."""
        logger.info("=== APPLICATION PHASE ===")

        # Run workers in parallel
        tasks = [
            worker.run_cycle()
            for worker in self.workers.values()
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)
        total = sum(r for r in results if isinstance(r, int))

        logger.info(f"Application phase complete: {total} jobs applied")
        return total

    async def run_full_cycle(self) -> Dict[str, int]:
        """Run complete research + application cycle."""
        stats = {
            "research": 0,
            "applied": 0,
            "timestamp": datetime.now().isoformat()
        }

        # Research phase
        stats["research"] = await self.run_research_phase()

        # Brief pause between phases
        await asyncio.sleep(5)

        # Application phase
        stats["applied"] = await self.run_application_phase()

        # Get final stats
        db_stats = await self.db.get_stats()
        stats.update(db_stats)

        return stats

    async def continuous_mode(self, interval_minutes: int = 120) -> None:
        """Run continuously with specified interval."""
        self._running = True

        logger.info(f"Starting continuous mode (interval: {interval_minutes}min)")

        while self._running:
            try:
                stats = await self.run_full_cycle()
                logger.info(f"Cycle complete: {stats}")

                # Wait for next cycle
                logger.info(f"Sleeping for {interval_minutes} minutes...")
                await asyncio.sleep(interval_minutes * 60)

            except Exception as e:
                logger.error(f"Cycle error: {e}")
                await asyncio.sleep(60)  # Brief retry on error

    def stop(self):
        """Signal continuous mode to stop."""
        self._running = False

    async def shutdown(self):
        """Shutdown all workers."""
        logger.info("Shutting down swarm...")
        for worker in self.workers.values():
            await worker.stop()
        self.workers.clear()

import asyncio
import logging
import os
import random
from datetime import datetime
from agents.research_agent import ResearchAgent
from agents.application_agent import ApplicationAgent
from agents.linkedin_agent import LinkedInAgent
from agents.profile_agent import ProfileAgent
from agents.tracker_agent import TrackerAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MasterOrchestrator:
    def __init__(self, mode="BALANCED"):
        self.mode = mode # AGGRESSIVE, BALANCED, CONSERVATIVE
        # V2 Limits
        self.daily_cap = 75 if mode == "AGGRESSIVE" else (60 if mode == "BALANCED" else 40)
        self.time_windows = [
            (9, 11),  # 9-11 AM
            (13, 15), # 1-3 PM
            (18, 21)  # 6-9 PM
        ]
        
        self.research_agent = ResearchAgent()
        self.apply_agent = ApplicationAgent()
        self.linkedin_agent = LinkedInAgent()
        self.profile_agent = ProfileAgent()
        self.tracker_agent = TrackerAgent()

    def is_within_window(self):
        now = datetime.now()
        hour = now.hour
        for start, end in self.time_windows:
            if start <= hour < end:
                return True
        return False

    def get_applied_today_count(self):
        import json
        if not os.path.exists("data/tracking.json"):
            return 0
        with open("data/tracking.json", "r") as f:
            try:
                data = json.load(f)
                today = datetime.now().strftime("%Y-%m-%d")
                return sum(1 for a in data.get("applications", []) if a.get("date_applied", "").startswith(today))
            except:
                return 0

    async def run_cycle(self, force_apply=False):
        logger.info(f"=== V2 ORCHESTRATOR: {self.mode} MODE ===")
        
        applied_today = self.get_applied_today_count()
        logger.info(f"Today's application count: {applied_today}/{self.daily_cap}")

        if applied_today >= self.daily_cap:
            logger.warning("Daily hard cap reached. Switching to RESEARCH-ONLY mode.")
            self.research_agent.scrape_all()
            return

        # V2 RULE: Apply only in specific time windows (unless forced)
        if not self.is_within_window() and not force_apply:
            logger.info("Outside of strategic time windows. Skipping application phase.")
            # Still perform research and profile maintenance
            self.research_agent.scrape_all()
            self.profile_agent.refresh_profiles()
            return

        if force_apply:
            logger.info("MANUAL OVERRIDE: Forcing application phase.")

        # Phase 4: Tracker
        self.tracker_agent.update_tracker()
        
        # Phase 5: Follow-Up Intelligence (V2 Lifecycle)
        self.tracker_agent.run_follow_ups()
        
        # Phase 1: Research
        self.research_agent.scrape_all()
        
        # Phase 2: Application (Agent 2)
        # V2 Rule: Distributed across time windows, no batching 30 in 20 mins
        await self.apply_agent.process_queue()
        
        # Phase 3: LinkedIn Strategic (Agent 3)
        # V2 Rule: Strategic outreach for high-priority jobs
        if os.path.exists("data/job_queue.json"):
            with open("data/job_queue.json", "r") as f:
                queue = json.load(f)
                high_priority_jobs = [j for j in queue if j.get("priority") == "HIGH" and j.get("status") == "applied"]
                for job in high_priority_jobs:
                    self.linkedin_agent.run_strategic_outreach(job)

        self.linkedin_agent.handle_recruiter_messages()
        
        logger.info("=== CYCLE COMPLETE ===")

async def main():
    orchestrator = MasterOrchestrator(mode="BALANCED")
    # In clinical mode, we'll run one cycle for verification
    # Passing force_apply=True specifically at user request
    await orchestrator.run_cycle(force_apply=True)

if __name__ == "__main__":
    asyncio.run(main())

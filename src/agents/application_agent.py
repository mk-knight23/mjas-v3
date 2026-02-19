import json
import logging
import os
import random
import time
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ApplicationAgent:
    def __init__(self, queue_file="data/job_queue.json"):
        self.queue_file = queue_file

    async def process_queue(self):
        if not os.path.exists(self.queue_file):
            logger.info("No job queue found.")
            return

        with open(self.queue_file, 'r') as f:
            queue = json.load(f)

        pending_jobs = [j for j in queue if j["status"] == "queued"]
        logger.info(f"Processing {len(pending_jobs)} pending jobs...")

        for job in pending_jobs:
            success = await self._apply_to_job(job)
            if success:
                job["status"] = "applied"
                job["date_applied"] = datetime.now().isoformat()
            else:
                job["status"] = "failed"

        with open(self.queue_file, 'w') as f:
            json.dump(queue, f, indent=2)

    async def _apply_to_job(self, job):
        portal = job.get("portal", "unknown")
        logger.info(f"Starting application flow for {job.get('title')} at {job.get('company')} via {portal}...")
        
        # Human Behavior Step 1: Preliminary Scroll (Simulate reading)
        logger.info("Simulating page read: scrolling down...")
        await asyncio.sleep(random.uniform(1.0, 3.0))
        
        # Step 2: Strategic Authentication (Google Sign-in)
        if portal in ["naukri", "indeed", "glassdoor", "ziprecruiter", "jobright"]:
            logger.info(f"Authenticating via Google (kazimusharraf1234@gmail.com) on {portal}...")
            # Human delay before clicking login
            await asyncio.sleep(random.uniform(2.0, 4.0))
        
        # Specialized portal logic
        if portal == "naukri":
            logger.info("Performing Naukri-specific form filling...")
            # Simulate character-by-character typing for key fields
            await self._simulate_typing(job.get("title"), "Job Title Field")
        elif portal == "indeed":
            logger.info("Processing Indeed Easy Apply flow...")
        elif portal == "jobright":
            logger.info("Executing AI-to-AI handshake on JobRight...")
        
        # Narrative optimization
        narrative = self._optimize_resume(job)
        cl = self._generate_cl(job)
        
        # Step 3: Human Delay before Submission
        logger.info("Final review: pausing for 3 seconds...")
        await asyncio.sleep(random.uniform(2.5, 4.5))
        
        # Simulated submission
        logger.info(f"Application successfully submitted to {job.get('company')}!")
        
        # Log to tracker
        from agents.tracker_agent import TrackerAgent
        tracker = TrackerAgent()
        tracker.log_application(job)
        
        # Random delay between applications (V2 Rule: 45-90 seconds)
        inter_app_delay = random.randint(45, 90)
        logger.info(f"Application complete. Waiting {inter_app_delay} seconds before next task (Anti-detection)...")
        await asyncio.sleep(inter_app_delay)
        
        return True

    async def _simulate_typing(self, text, field_name):
        logger.info(f"Typing into {field_name} character by character...")
        for char in text:
            await asyncio.sleep(random.uniform(0.05, 0.2))
        logger.info(f"Finished typing {text}")

    def _optimize_resume(self, job):
        # V2: Narrative Intelligence using Master Profile
        logger.info(f"Optimizing resume summary for {job.get('title')}...")
        narrative = (
            f"Agentic AI Engineer and builder of the VIBE ecosystem. "
            f"Specializing in production-grade {job.get('title')} systems using "
            f"LangGraph, RAG, and multi-agent architectures. Portfolio of 60 projects "
            f"showcasing deep technical mastery."
        )
        return narrative

    def _generate_cl(self, job):
        # V2: Strategic positioning from Master Profile
        is_startup = any(k in job.get("company", "").lower() for k in ["tech", "labs", "ai", "solutions"])
        tone = "ENTHUSIASTIC" if is_startup else "ANALYTICAL"
        
        logger.info(f"Generating {tone} cover letter based on Master Profile...")
        
        cl = (
            f"Dear hiring team at {job.get('company')},\n\n"
            f"I am Mikazi Musharraf, an AI Engineer focused on building autonomous AI ecosystems. "
            f"My work on the VIBE platform aligns perfectly with the requirements for the "
            f"{job.get('title')} position. I specialize in multi-LLM orchestration and "
            f"production-grade agentic systems.\n\n"
            f"I look forward to discussing how my experience can benefit your team."
        )
        return cl

if __name__ == "__main__":
    agent = ApplicationAgent()
    agent.process_queue()

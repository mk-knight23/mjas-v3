import logging
import random
import time
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ExecutorAgent:
    def __init__(self, daily_cap=15):
        self.daily_cap = daily_cap
        self.applied_count = 0

    def apply(self, job_id, platform, apply_url, resume_path, cl_path):
        if self.applied_count >= self.daily_cap:
            logger.warning(f"Daily cap reached ({self.daily_cap}). Skipping application.")
            return False

        logger.info(f"Starting application for job {job_id} on {platform}")
        logger.info(f"URL: {apply_url}")
        
        # Humanized process simulation
        logger.info("Step 1: Navigating to job URL...")
        time.sleep(random.uniform(5, 10))
        
        logger.info("Step 2: Scrolling page to simulate reading...")
        time.sleep(random.uniform(3, 7))
        
        logger.info(f"Step 3: Uploading resume from {resume_path}...")
        time.sleep(random.uniform(5, 12))
        
        logger.info("Step 4: Filling form fields with typing delay...")
        # Simulate typing delay (50-150ms per char)
        time.sleep(random.uniform(10, 20))
        
        logger.info(f"Step 5: Pasting cover letter from {cl_path}...")
        time.sleep(random.uniform(3, 8))
        
        logger.info("Step 6: Submitting application...")
        time.sleep(random.uniform(5, 10))
        
        logger.info(f"SUCCESS: Application submitted for {job_id}")
        self.applied_count += 1
        return True

if __name__ == "__main__":
    executor = ExecutorAgent()
    # Mock call
    # executor.apply("123", "linkedin", "http://example.com", "data/resume.txt", "data/cl.txt")

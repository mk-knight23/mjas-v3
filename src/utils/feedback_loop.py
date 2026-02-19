import json
import logging
import os
import re
from collections import Counter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AdaptiveFeedbackLoop:
    def __init__(self, queue_file="data/job_queue.json"):
        self.queue_file = queue_file

    def optimize_keywords(self):
        if not os.path.exists(self.queue_file):
            return

        with open(self.queue_file, 'r') as f:
            queue = json.load(f)

        # V2: Analyze top 20 job descriptions/titles
        top_jobs = sorted(queue, key=lambda x: x.get("score", 0), reverse=True)[:20]
        
        words = []
        for job in top_jobs:
            # Simple word extraction from titles for demonstration
            words.extend(re.findall(r'\w+', job.get("title", "").lower()))
        
        common = Counter(words).most_common(10)
        logger.info(f"V2 ADAPTIVE: Extracted common keywords from top leads: {common}")
        
        # In a real scenario, this would update config/candidate_profile.yaml
        return common

if __name__ == "__main__":
    loop = AdaptiveFeedbackLoop()
    loop.optimize_keywords()

import json
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TrackingAgent:
    def __init__(self, tracking_file="data/tracking.json"):
        self.tracking_file = tracking_file
        self.tracking_data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.tracking_file):
            with open(self.tracking_file, 'r') as f:
                return json.load(f)
        return {"applications": [], "stats": {"rejections": 0, "interviews": 0, "total": 0}}

    def log_application(self, job):
        entry = {
            "job_id": job.get("job_id"),
            "company": job.get("company"),
            "role": job.get("role"),
            "platform": job.get("platform"),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Submitted",
            "score": job.get("score")
        }
        self.tracking_data["applications"].append(entry)
        self.tracking_data["stats"]["total"] += 1
        self._save_data()
        logger.info(f"Logged application for {job.get('job_id')}")

    def _save_data(self):
        os.makedirs(os.path.dirname(self.tracking_file), exist_ok=True)
        with open(self.tracking_file, 'w') as f:
            json.dump(self.tracking_data, f, indent=2)

if __name__ == "__main__":
    tracker = TrackingAgent()
    tracker.log_application({"job_id": "mock_id", "company": "Mock Corp", "role": "Mock AI Engineer", "platform": "linkedin", "score": 90})

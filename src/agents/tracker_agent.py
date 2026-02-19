import json
import logging
import os
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TrackerAgent:
    def __init__(self, tracker_file="data/tracking.json", queue_file="data/job_queue.json"):
        self.tracker_file = tracker_file
        self.queue_file = queue_file

    def update_tracker(self):
        if not os.path.exists(self.queue_file):
            return

        with open(self.queue_file, 'r') as f:
            queue = json.load(f)

        if os.path.exists(self.tracker_file):
            with open(self.tracker_file, 'r') as f:
                tracker_data = json.load(f)
        else:
            tracker_data = {"applications": [], "stats": {"total": 0, "applied": 0, "failed": 0}}

        applied_jobs = [j for j in queue if j["status"] == "applied"]
        current_ids = {a.get("job_url") for a in tracker_data["applications"]}

        for job in applied_jobs:
            if job["url"] not in current_ids:
                self.log_application(job)

    def log_application(self, job):
        os.makedirs(os.path.dirname(self.tracker_file), exist_ok=True)
        if os.path.exists(self.tracker_file):
            with open(self.tracker_file, 'r') as f:
                data = json.load(f)
        else:
            data = {"applications": [], "stats": {"total": 0, "applied": 0}}

        app_id = f"APP-{datetime.now().strftime('%Y%m%d')}-{len(data['applications'])+1:03d}"
        entry = {
            "application_id": app_id,
            "date_applied": datetime.now().strftime("%Y-%m-%d"),
            "time_applied": datetime.now().strftime("%H:%M:%S"),
            "company": job.get("company"),
            "job_title": job.get("title"),
            "portal": job.get("portal"),
            "job_url": job.get("url"),
            "status": "applied",
            "score": job.get("score", 0),
            "follow_up_1": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "follow_up_2": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
            "notes": "V2 High-Precision Application"
        }
        
        data["applications"].append(entry)
        data["stats"]["applied"] += 1
        data["stats"]["total"] += 1
        
        with open(self.tracker_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"V2 TRACKER: Logged {app_id} for {job.get('company')}. Follow-ups scheduled.")

    def run_follow_ups(self):
        logger.info("Checking for pending follow-ups...")
        today = datetime.now().strftime("%Y-%m-%d")
        
        if not os.path.exists(self.tracker_file):
            return

        with open(self.tracker_file, 'r') as f:
            data = json.load(f)

        for app in data["applications"]:
            if app["status"] == "applied":
                if app.get("follow_up_1") == today:
                    self._send_follow_up(app, 1)
                elif app.get("follow_up_2") == today:
                    self._send_follow_up(app, 2)

    def _send_follow_up(self, app, stage):
        logger.info(f"SENDING FOLLOW-UP {stage} for {app['job_title']} at {app['company']}...")
        # Simulated email sending
        time.sleep(1)
        logger.info(f"Follow-up {stage} email successfully simulated for {app['company']}.")

    def generate_daily_report(self):
        if not os.path.exists(self.tracker_file):
            return "No tracking data available."

        with open(self.tracker_file, 'r') as f:
            data = json.load(f)

        apps = data.get("applications", [])
        if not apps:
            return "No applications logged."

        # V2 Intelligence Core: Compute Statistics
        stats = {
            "by_portal": {},
            "by_title": {},
            "total": len(apps)
        }

        for app in apps:
            portal = app.get("portal")
            title = app.get("job_title")
            status = app.get("status")

            # Portal stats
            if portal not in stats["by_portal"]:
                stats["by_portal"][portal] = {"total": 0, "responses": 0}
            stats["by_portal"][portal]["total"] += 1
            if status in ["interview", "viewed"]:
                stats["by_portal"][portal]["responses"] += 1

        # V2 Rule: Adaptive Weighting
        for portal, p_stats in stats["by_portal"].items():
            rate = (p_stats["responses"] / p_stats["total"]) * 100
            if p_stats["total"] >= 10 and rate < 3:
                logger.warning(f"ADAPTIVE: Portal {portal} response rate is low ({rate:.1f}%). Recommending weight reduction.")

        return stats

if __name__ == "__main__":
    agent = TrackerAgent()
    agent.update_tracker()

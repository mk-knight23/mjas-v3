import json
import logging
import re
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MatchingAgent:
    def __init__(self, resume_path):
        self.resume_path = resume_path
        self.resume_text = self._load_resume()
        self.skills = self._extract_skills(self.resume_text)

    def _load_resume(self):
        # In a real scenario, this would parse PDF/Docx. 
        # For now, we'll assume a text file or common keywords.
        if os.path.exists(self.resume_path):
            with open(self.resume_path, 'r') as f:
                return f.read().lower()
        return ""

    def _extract_skills(self, text):
        # Simple keyword-based extraction for demonstration
        common_skills = ["python", "ai", "llm", "generative ai", "genai", "agentic ai", "machine learning", "nlp", "pytorch", "tensorflow", "fastapi", "docker", "aws"]
        found_skills = [skill for skill in common_skills if skill in text]
        return found_skills

    def score_job(self, job):
        jd_text = job.get("jd_text", "").lower() or job.get("role", "").lower()
        
        # Scoring Formula:
        # score = (skill_overlap * 0.5) + (experience_match * 0.2) + (location_match * 0.1) + (title_similarity * 0.2)
        
        # 1. Skill Overlap
        required_skills = [skill for skill in self.skills if skill in jd_text]
        skill_score = (len(required_skills) / len(self.skills)) * 100 if self.skills else 0
        
        # 2. Experience Match (Dummy for now)
        exp_score = 80 # Assume 80 for now
        
        # 3. Location Match
        loc_match = 100 if "remote" in job.get("location", "").lower() or "india" in job.get("location", "").lower() else 50
        
        # 4. Title Similarity
        target_titles = ["ai engineer", "python developer", "generative ai", "llm engineer"]
        title_score = 100 if any(t in job.get("role", "").lower() for t in target_titles) else 50
        
        total_score = (skill_score * 0.5) + (exp_score * 0.2) + (loc_match * 0.1) + (title_score * 0.2)
        
        decision = "REJECT"
        if total_score > 85:
            decision = "AUTO-APPROVE"
        elif total_score >= 70:
            decision = "OPTIMIZE"
            
        return {
            "job_id": job.get("job_id"),
            "score": total_score,
            "missing_skills": [s for s in self.skills if s not in jd_text],
            "decision": decision
        }

    def process_jobs(self, jobs_file="data/jobs.json", output_file="data/scored_jobs.json"):
        if not os.path.exists(jobs_file):
            logger.error(f"{jobs_file} not found")
            return

        with open(jobs_file, 'r') as f:
            jobs = json.load(f)

        scored_jobs = []
        for job in jobs:
            scored_job = self.score_job(job)
            scored_jobs.append({**job, **scored_job})

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(scored_jobs, f, indent=2)
        logger.info(f"Scored {len(scored_jobs)} jobs and saved to {output_file}")

if __name__ == "__main__":
    # Create a dummy resume for testing
    dummy_resume = "data/resume.txt"
    os.makedirs("data", exist_ok=True)
    with open(dummy_resume, "w") as f:
        f.write("Python, AI, LLM, Generative AI, GenAI, Agentic AI, Machine Learning, FastAPI, Docker, AWS")
    
    matcher = MatchingAgent(dummy_resume)
    matcher.process_jobs()

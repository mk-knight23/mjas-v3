import json
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OptimizerAgent:
    def __init__(self, template_resume_path, template_cl_path):
        self.template_resume_path = template_resume_path
        self.template_cl_path = template_cl_path

    def _load_template(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                return f.read()
        return ""

    def optimize(self, job, scored_job):
        logger.info(f"Optimizing for job: {job.get('role')} at {job.get('company')}")
        
        # 1. Customize Resume (Simulated)
        # In a real scenario, this would use an LLM to rephrase and inject keywords
        resume_template = self._load_template(self.template_resume_path)
        optimized_resume = resume_template.replace("[ROLE]", job.get("role"))
        optimized_resume = optimized_resume.replace("[COMPANY]", job.get("company"))
        
        for skill in scored_job.get("missing_skills", []):
            if skill in ["python", "ai", "llm"]: # Only inject if safe
                optimized_resume += f"\n- Proficient in {skill.capitalize()}"

        # 2. Generate Cover Letter (Simulated)
        cl_template = self._load_template(self.template_cl_path)
        optimized_cl = cl_template.replace("[ROLE]", job.get("role"))
        optimized_cl = optimized_cl.replace("[COMPANY]", job.get("company"))
        optimized_cl = optimized_cl.replace("[SKILLS]", ", ".join(scored_job.get("missing_skills", [])[:3]))

        # Save outputs
        output_dir = f"data/applications/{job.get('job_id')}"
        os.makedirs(output_dir, exist_ok=True)
        
        with open(f"{output_dir}/resume.txt", "w") as f:
            f.write(optimized_resume)
        
        with open(f"{output_dir}/cover_letter.txt", "w") as f:
            f.write(optimized_cl)
            
        logger.info(f"Optimization complete for {job.get('job_id')}")
        return {
            "resume_path": f"{output_dir}/resume.txt",
            "cl_path": f"{output_dir}/cover_letter.txt"
        }

    def process_approved_jobs(self, scored_jobs_file="data/scored_jobs.json"):
        if not os.path.exists(scored_jobs_file):
            logger.error(f"{scored_jobs_file} not found")
            return

        with open(scored_jobs_file, 'r') as f:
            scored_jobs = json.load(f)

        for s_job in scored_jobs:
            if s_job.get("decision") in ["AUTO-APPROVE", "OPTIMIZE"]:
                self.optimize(s_job, s_job)

if __name__ == "__main__":
    # Create templates
    os.makedirs("data/templates", exist_ok=True)
    with open("data/templates/resume_template.txt", "w") as f:
        f.write("Mikazi Musharraf\nAI Engineer\nApplying for [ROLE] at [COMPANY]\nExperience: 3 years in AI/Python.")
    
    with open("data/templates/cl_template.txt", "w") as f:
        f.write("Dear Hiring Manager at [COMPANY],\nI am excited to apply for the [ROLE] position. I have strong skills in [SKILLS].")
    
    optimizer = OptimizerAgent("data/templates/resume_template.txt", "data/templates/cl_template.txt")
    optimizer.process_approved_jobs()

# Job Matching & Scoring Agent

## Objective
Score job fit before application.

## Scoring Threshold
Reject < 70
Optimize 70–85
Auto-approve > 85

## Inputs
- Resume
- JD text

## Output
{
  job_id,
  score,
  missing_skills,
  decision
}

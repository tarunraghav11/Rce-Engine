from redis_queue import pop_task, set_job_status
from executor import execute_code
from db import SessionLocal, Job
from datetime import datetime, timezone

print("Worker started. Waiting for jobs...")

while True:
    task = pop_task()  

    if not task:
        continue

    job_id = task["job_id"]
    code = task["code"]

    db = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        db.close()
        continue

    job.status = "running"
    db.commit()

    result = execute_code(code)

    job.status = result["status"]
    job.output = result["output"]
    job.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.close()

    print(f"Finished job {job_id}")

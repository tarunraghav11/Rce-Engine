import uuid
from backend.redis_queue import push_task, set_job_status

if __name__ == "__main__":

    job_id = str(uuid.uuid4())
    job = {
        "job_id": job_id,
        "language": "python",
        "code": 'while True : pass'
    }
    
    set_job_status(job_id, "queued")
    push_task(job)
    
    print(f"Submitted job: {job_id}")
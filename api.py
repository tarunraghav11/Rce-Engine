from fastapi import FastAPI
import uuid 
from db import SessionLocal , Job
from redis_queue import push_task , set_job_status , get_job_status

app = FastAPI()

@app.post("/submit")

def submit_code(payload: dict):
    code = payload.get("code")

    if not code:
        return {"error": "Code not provided"}
    
    job_id = str(uuid.uuid4())

    db = SessionLocal()
    job = Job(
        id = job_id,
        code = code,
        status = "queued",
        output = ""
    )

    db.add(job)
    db.commit()
    db.close()

    push_task(
        {
            "job_id": job_id,
            "code": code
        }
    )

    return {"job_id": job_id,
            "status": "queued"
           }

@app.get("/status/{job_id}")
def get_status(job_id: str):
    db = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()
    db.close()

    if not job:
        return {"error": "Job not found"}

    return {
        "status": job.status,
        "output": job.output
    }

from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import uuid 
from db import SessionLocal, Job, init_db
from redis_queue import push_task
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/submit")
def submit_code(payload: dict):
    code = payload.get("code", "").strip()
    
    if not code:
        raise HTTPException(status_code=400, detail="Code not provided")
    
    job_id = str(uuid.uuid4())
    db = SessionLocal()
    
    try:
        job = Job(id=job_id, code=code, status="queued", output="")
        db.add(job)
        db.commit()
        push_task({"job_id": job_id, "code": code})
        return {"job_id": job_id, "status": "queued"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error submitting job: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit job")
    finally:
        db.close()

@app.get("/status/{job_id}")
def get_status(job_id: str):
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return {"status": job.status, "output": job.output}
    finally:
        db.close()

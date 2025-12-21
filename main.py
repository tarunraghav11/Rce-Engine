from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CodeSubmission(BaseModel):
    language:str
    code: str

@app.post("/submit")
async def submit_code(submission: CodeSubmission):
    if not submission.code.strip():
        return {"status": "error", "message": "Code cannot be empty."}
    
    return {
        "job_id": "12345",
        "status": "pending"
    }
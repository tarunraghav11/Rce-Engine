from redis_queue import pop_task, set_job_status
from executor import execute_code

print("Worker started. Waiting for jobs...")

while True:
    task = pop_task()  

    if not task:
        continue

    job_id = task["job_id"]
    code = task["code"]

    print(f"Picked up job {job_id}")

    set_job_status(job_id, "running")

    result = execute_code(code)

    if result["status"] == "success":
        set_job_status(job_id, "success", result["output"])
    else:
        set_job_status(job_id, "error", result["output"])

    print(f"Finished job {job_id}")

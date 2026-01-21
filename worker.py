from redis_queue import pop_task
from executor import execute_code

while True:
    task = pop_task()

    if not task:
        continue
    
    code = task.get("code")

    result = execute_code(code)

    print("execution result: ")
    print(result)
    
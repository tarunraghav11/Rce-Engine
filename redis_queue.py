import redis
import json

REDIS_HOST = "localhost"
REDIS_PORT = 6379
QUEUE_NAME = "code_tasks"

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

def push_task(task: dict):
    
    #Producer pushes a job into the queue.
    
    redis_client.rpush(QUEUE_NAME, json.dumps(task))


def pop_task():
    
    #Worker blocks until a job is available.
    
    task = redis_client.blpop(QUEUE_NAME)
    if task:
        _, data = task
        return json.loads(data)
    return None

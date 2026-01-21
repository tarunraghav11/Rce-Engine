from redis_queue import push_task

if __name__ == "__main__":
    job = {
        "language": "python",
        "code": 'print("Hello from the producer!")'
    }

    push_task(job)
    print("Job pushed to the queue.")
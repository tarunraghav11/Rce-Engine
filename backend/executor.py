import docker
from docker.errors import ContainerError
import time

client = docker.from_env()

def execute_code(code: str,timeout: int = 3):
    container = None
    try:
        wrapped_code = code
        container = client.containers.run(
    image="python:3.9-alpine",
    command=["python", "-c", wrapped_code],
    detach=True,
    stdout=True,
    stderr=True,

    network_mode="none",
    read_only=True,
    user="1000:1000",
    cap_drop=["ALL"],
    pids_limit=64,
    tmpfs={"/tmp": "rw,noexec,nosuid,size=16m"},

    mem_limit="128m",
    cpu_period=100000,
    cpu_quota=50000,
)


        start = time.time()
        while True:
            container.reload()
            if container.status == "exited":
                logs = container.logs().decode("utf-8")
                container.remove()
                return {
                    "status": "success",
                    "output": logs      
                }

            if time.time() - start > timeout:
                container.kill()
                container.remove()
                return {
                    "status" : "error",
                    "output": f"Execution exceeded {timeout} seconds"
                }
            
            time.sleep(0.1)

    except ContainerError as e:
        return {
            "status": "error",
            "output": e.stderr.decode("utf-8")
        }




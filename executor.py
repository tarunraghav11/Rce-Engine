import docker
from docker.errors import ContainerError
import time

client = docker.from_env()

def execute_code(code: str,timeout: int = 3):
    container = None
    try:
        container = client.containers.run(
            image="python:3.9-alpine",
            command=["python", "-c", code],
            network_disabled=True,
            mem_limit="128m",
            user = "1000:1000",
            read_only=True,
            cpu_period=100000,
            cpu_quota=50000,
            detach=True,
            stdout=True,
            stderr=True
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




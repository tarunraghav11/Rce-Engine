import docker
from docker.errors import ContainerError

client = docker.from_env()

def execute_code(code: str):
    try:
        output = client.containers.run(
            image="python:3.9-alpine",
            command=["python", "-c", code],
            remove=True,
            network_disabled=True,
            mem_limit="128m",
            stdout=True,
            stderr=True
        )

        return {
            "status": "success",
            "output": output.decode("utf-8")
        }

    except ContainerError as e:
        return {
            "status": "error",
            "output": e.stderr.decode("utf-8")
        }


if __name__ == "__main__":
    result = execute_code('print("Hello, World!")')
    print(result)

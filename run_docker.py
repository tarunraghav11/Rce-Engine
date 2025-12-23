import docker

def execute_code(code: str):
    client = docker.from_env()

    output = client.containers.run(
        image="python:3.9-alpine",
        command=["python", "-c", code],
        remove=True
    )

    return output.decode("utf-8")


if __name__ == "__main__":
    sample_code = 'print("Hello, World!")'
    result = execute_code(sample_code)
    print(result)

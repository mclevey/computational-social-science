import os
import subprocess
import sys


def run_docker():
    if not os.path.isfile("pyproject.toml"):
        print(
            (
                "Error: 'pyproject.toml' not found. Please run "
                "this script from the project root directory."
            )
        )
        sys.exit(1)

    project_root = os.getcwd()

    try:
        subprocess.run(
            [
                "docker",
                "run",
                "-it",
                "--rm",
                "-v",
                f"{project_root}:/app",
                "-w",
                "/app",
                "gesis",
                "zsh",
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"{e}\nBuilding Docker Image")
        build_docker_image()
        run_docker()


def build_docker_image():
    try:
        subprocess.run(
            ["docker", "build", "-f", "Dockerfile", "-t", "gesis", "."], check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Failed to build Docker image: {e}")


if __name__ == "__main__":
    run_docker()

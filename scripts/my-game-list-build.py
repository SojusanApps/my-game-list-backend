#!/usr/bin/env python
# ruff: noqa: S603, S607
import glob
import inspect
import shutil
import subprocess
import sys
from distutils.util import strtobool
from itertools import chain
from pathlib import Path

from python_colors import print_error, print_info, print_warning

import docker
from docker.errors import BuildError

DOCKER_LOGS_STREAM_VALUE = "stream"
DOCKER_LOGS_ERROR_VALUE = "errorDetail"
DOCKER_REGISTRY = "ghcr.io"
DOCKER_REGISTRY_PATH_APP = f"{DOCKER_REGISTRY}/sojusan/my-game-list/app"
DOCKER_REGISTRY_PATH_NGINX = f"{DOCKER_REGISTRY}/sojusan/my-game-list/nginx"
FAILURE_CODE = 1


docker_client = docker.from_env()


def setup_project(path: str = "dist") -> None:
    """Create whl file for the project.

    Args:
        path (str, optional): Path where .whl will be distributed. Defaults to 'dist'.
    """
    print_info("Whl file creation started.")
    subprocess.Popen(["python", "setup.py", "bdist_wheel", f"--dist-dir={path}"]).wait()
    print_info("Whl file creation finished.")


def clean_up(dist_path: str = "dist") -> None:
    """Cleaning after build project.

    Args:
        dist_path (str, optional): A path where .whl was distributed. A value set to None or 'None'
            prevents to remove dist directory. Defaults to 'dist'.
    """
    print_info("Cleaning after build project started.")
    subprocess.Popen(["python", "setup.py", "clean", "--all"]).wait()
    build_dir = ("build/",)
    egg_info_dir = glob.glob("*.egg-info/")
    dist_dir = () if not dist_path or dist_path == "None" else (dist_path,)

    for dir_path in chain(build_dir, egg_info_dir, dist_dir):
        if Path(dir_path).is_dir():
            shutil.rmtree(dir_path)

    print_info("Cleaning finished.")


def remove_whls(path: str = "dist") -> None:
    """Remove all whl files.

    Args:
        path (str, optional): Path to whl files. Defaults to 'dist'.
    """
    print_info("Removing of the whl files started.")

    for whl_file in glob.glob(f"{path}/*.whl"):
        Path(whl_file).unlink()

    print_info("Removing finished.")


def _build_docker_image(path: str, tag: str):
    print_info("Image building has begun (it will take a while)...")
    try:
        image, image_build_logs = docker_client.images.build(path=path, tag=tag)
    except BuildError as exception:
        print_error("Something went wrong while building!")
        for line in exception.build_log:
            if DOCKER_LOGS_STREAM_VALUE in line:
                print_error(line[DOCKER_LOGS_STREAM_VALUE].strip())
        raise
    else:
        for line in image_build_logs:
            if DOCKER_LOGS_STREAM_VALUE in line:
                print(line[DOCKER_LOGS_STREAM_VALUE].strip())
        print_info(f"Docker image was build: {image}")


def build_app(tag: str = "latest", clean: str = "true") -> None:
    """Build a web application container.

    Args:
        tag (str, optional): Tag for a built web application container. Defaults to 'latest'.
        clean (str, optional): Cleaning after building. Defaults to 'true'.

    Raises:
        ValueError: If clean value is incorrect.
    """
    print_info("Build app container - started.")
    app_directory = Path("docker", "app")
    clean_up(None)
    remove_whls(app_directory)
    setup_project(app_directory)
    _build_docker_image(str(app_directory), f"{DOCKER_REGISTRY_PATH_APP}:{tag}")

    try:
        if strtobool(clean):
            clean_up(None)
            remove_whls(app_directory)
    except ValueError:
        print_error("Wrong passed parameter for clean. Cleaning won't be executed.")
        raise

    print_info("Build app container - finished.")


def build_nginx(tag: str = "latest") -> None:
    """Build an Nginx container.

    Args:
        tag (str, optional): Tag for a built Nginx container. Defaults to 'latest'.
    """
    print_info("Build nginx container - started.")
    nginx_directory = Path("docker", "nginx")
    _build_docker_image(str(nginx_directory), f"{DOCKER_REGISTRY_PATH_NGINX}:{tag}")
    print_info("Build nginx container - finished.")


def build_images(tag: str = "latest") -> None:
    """Build all containers for a project (app, Nginx).

    Args:
        tag (str, optional): Tag for built containers. Defaults to 'latest'.
    """
    build_app(tag)
    build_nginx(tag)


def _push_docker_image(repository: str, tag: str):
    print_info("Image pushing has begun (it will take a while)...")
    response = docker_client.images.push(
        repository=repository,
        tag=tag,
        stream=True,
        decode=True,
    )

    for line in response:
        print(line)
        if DOCKER_LOGS_ERROR_VALUE in line:
            print_error(line)
            print_warning(
                "Remember that in order to be able to push images on GitHub, you must log in to the registry "
                "using the `Personal access token` as a password. This token needs to have permission "
                "to manage packages.",
            )
            sys.exit(FAILURE_CODE)

    print_info("Docker image has been pushed.")


def push_app(tag: str = "latest") -> None:
    """Push a docker web container to the registry.

    Args:
        tag (str, optional): Tag for a pushed web container. Defaults to 'latest'.
    """
    print_info("Pushing app package ...")
    _push_docker_image(DOCKER_REGISTRY_PATH_APP, tag)


def push_nginx(tag: str = "latest") -> None:
    """Push a docker Nginx container to the registry.

    Args:
        tag (str, optional): Tag for a pushed Nginx container. Defaults to 'latest'.
    """
    print_info("Pushing nginx package ...")
    _push_docker_image(DOCKER_REGISTRY_PATH_NGINX, tag)


def push_images(tag: str = "latest") -> None:
    """Push all built containers(web, Nginx) to the registry.

    Args:
        tag (str, optional): Tag for built containers. Defaults to 'latest'.
    """
    push_app(tag)
    push_nginx(tag)


def docker_up() -> None:
    """Docker-compose up with default configuration."""
    docker_compose_path = Path("docker", "docker-compose.yml")
    subprocess.Popen(["docker", "compose", "-f", f"{str(docker_compose_path)}", "up"]).wait()


def docker_build_and_up() -> None:
    """Build all images and docker-compose up with default configuration."""
    build_images()
    docker_up()


def get_module_functions_names() -> dict[str, object]:
    """Get available functions.

    Returns all the defined function names in this module.
    In the case of security, users should be allowed to only call functions
    that were defined in this file.

    Returns:
        A dictionary contains the name of the function as key and the function
        reference as value.
    """
    return {
        name: obj
        for name, obj in inspect.getmembers(sys.modules[__name__])
        if (inspect.isfunction(obj) and obj.__module__ == __name__)
        and name not in ("main", "get_module_functions_names")
        and not name.startswith("_")
    }


def main() -> int:
    """Run the build tasks."""
    available_functions = get_module_functions_names()

    for arg in sys.argv[1:]:
        # arguments for function are passed by using the concatenation of ":" with
        # the function name and arguments e.g: function:arg1:arg2
        function_args = arg.split(":")
        if (function_name := function_args[0]) in available_functions:
            available_functions[function_name](*function_args[1:])
        else:
            print_warning(f"Missing function with a name: {function_name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

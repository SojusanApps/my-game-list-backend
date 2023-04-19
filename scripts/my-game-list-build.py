#!/usr/bin/env python
import inspect
import json
import os
import sys
from distutils.util import strtobool
from pathlib import Path

from python_colors import print_error, print_warning

DOCKER_REGISTRY = "docker.pkg.github.com"
DOCKER_REGISTRY_PATH_WEB = f"{DOCKER_REGISTRY}/sojusan/my-game-list/app"
DOCKER_REGISTRY_PATH_NGINX = f"{DOCKER_REGISTRY}/sojusan/my-game-list/nginx"


def setup_project(path: str = "dist") -> None:
    """Create whl file for the project.

    Args:
        path (str, optional): Path where .whl will be distributed. Defaults to 'dist'.
    """
    os.system(f"python setup.py bdist_wheel --dist-dir={path}")


def clean_up(dist_path: str = "dist") -> None:
    """Cleaning after build project.

    Args:
        dist_path (str, optional): A path where .whl was distributed. A value set to None or 'None'
            prevents to remove dist directory. Defaults to 'dist'.
    """
    os.system("python setup.py clean --all")
    os.system(f'rm -rf build/ *.egg-info/ {"" if not dist_path or dist_path == "None" else dist_path}')


def remove_whls(path: str = "dist/") -> None:
    """Remove all whl files.

    Args:
        path (str, optional): Path to whl files. Defaults to 'dist/'.
    """
    os.system(f"rm -f {path}*.whl")


def build_app(tag: str = "latest", clean: str = "true") -> None:
    """Build a web application container.

    Args:
        tag (str, optional): Tag for a built web application container. Defaults to 'latest'.
        clean (str, optional): Cleaning after building. Defaults to 'true'.

    Raises:
        ValueError: If clean value is incorrect.
    """
    app_directory = "docker/app/"
    clean_up(None)
    remove_whls(app_directory)
    setup_project(app_directory)
    os.system(f"cd {app_directory} && docker build . -t {DOCKER_REGISTRY_PATH_WEB}:{tag}")
    try:
        if strtobool(clean):
            clean_up(None)
            remove_whls(app_directory)
    except ValueError:
        print_error("Wrong passed parameter for clean. Cleaning won't be executed.")
        raise


def build_nginx(tag: str = "latest") -> None:
    """Build an Nginx container.

    Args:
        tag (str, optional): Tag for a built Nginx container. Defaults to 'latest'.
    """
    os.system(f"cd docker/nginx && docker build . -t {DOCKER_REGISTRY_PATH_NGINX}:{tag}")


def build_images(tag: str = "latest") -> None:
    """Build all containers for a project (app, Nginx).

    Args:
        tag (str, optional): Tag for built containers. Defaults to 'latest'.
    """
    build_app(tag)
    build_nginx(tag)


def push_app(tag: str = "latest") -> None:
    """Push a docker web container to the registry.

    Args:
        tag (str, optional): Tag for a pushed web container. Defaults to 'latest'.
    """
    _login_to_docker_registry()
    os.system(f"docker push {DOCKER_REGISTRY_PATH_WEB}:{tag}")


def push_nginx(tag: str = "latest") -> None:
    """Push a docker Nginx container to the registry.

    Args:
        tag (str, optional): Tag for a pushed Nginx container. Defaults to 'latest'.
    """
    _login_to_docker_registry()
    os.system(f"docker push {DOCKER_REGISTRY_PATH_NGINX}:{tag}")


def push_images(tag: str = "latest") -> None:
    """Push all built containers(web, Nginx) to the registry.

    Args:
        tag (str, optional): Tag for built containers. Defaults to 'latest'.
    """
    push_app(tag)
    push_nginx(tag)


def docker_up() -> None:
    """Docker-compose up with default configuration."""
    os.system("docker-compose -f docker/docker-compose.yml up")


def docker_build_and_up() -> None:
    """Build all images and docker-compose up with default configuration."""
    build_images()
    docker_up()


def _is_docker_registry_access() -> bool:
    """Check if a user is logged into the docker registry."""
    try:
        path = f"{Path.home()}/.docker/config.json"
        with open(path) as docker_config_file:
            config_file: dict = json.load(docker_config_file)
            if authorizations := config_file.get("auths"):
                return authorizations.get(sys.argv[1]) is not None
            return False
    except FileNotFoundError:
        return False


def _login_to_docker_registry() -> None:
    """Login to the docker registry if required."""
    if not _is_docker_registry_access():
        answer = (
            input(f"Access to the docker registry is required, do you want to login to '{DOCKER_REGISTRY}' [y/n]?")
            or "y"
        )
        if answer == "y":
            os.system(f"docker login {DOCKER_REGISTRY}")
        else:
            print_error("Exiting: can't continue without login to the docker registry.")
            sys.exit(1)


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

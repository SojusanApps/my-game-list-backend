from os import path

from setuptools import find_packages, setup

from my_game_list import __version__

NAME = "my_game_list"
DESCRIPTION = "MyGameList API - Application to manage game lists."


def get_version():
    return ".".join(map(str, __version__))


def get_packages():
    packages = [f"{NAME}.{pkg}" for pkg in find_packages(NAME, exclude=("*.tests"))]
    return [NAME, "requirements"] + packages


CONFIG = {
    "name": "my-game-list",
    "version": get_version(),
    "description": DESCRIPTION,
    "packages": get_packages(),
    "include_package_data": True,
    "author": "Sojusan",
    "author_email": "grzegorczyk1rafal@gmail.com",
    "url": "https://github.com/Sojusan/my-game-list",
    "license": "proprietary",
    "classifiers": [
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.10",
        "License :: Other/Proprietary License",
    ],
    "scripts": [
        path.join("scripts", "my-game-list-manage.py"),
        path.join("scripts", "my-game-list-run-tests-with-pg.sh"),
        path.join("scripts", "my-game-list-run-tests.sh"),
        path.join("scripts", "my-game-list-build.py"),
        path.join("scripts", "wait-for-it.sh"),
    ],
}

setup(**CONFIG)

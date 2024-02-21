"""This module is responsible for configuring the project package."""
from pathlib import Path

from setuptools import find_packages, setup

from my_game_list import __version__

NAME = "my_game_list"
DESCRIPTION = "MyGameList API - Application to manage game lists."
LONG_DESCRIPTION = (Path(__file__).parent / "README.md").read_text()


def get_version() -> str:
    """Get the version of the application."""
    return ".".join(map(str, __version__))


def get_packages() -> list[str]:
    """Get the list of packages."""
    packages = [f"{NAME}.{pkg}" for pkg in find_packages(NAME, exclude=("*.tests"))]
    return [NAME, "requirements", *packages]


setup(
    name="my-game-list",
    version=get_version(),
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=get_packages(),
    include_package_data=True,
    author="Sojusan",
    author_email="grzegorczyk1rafal@gmail.com",
    url="https://github.com/Sojusan/my-game-list",
    license="proprietary",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.12",
        "License :: Other/Proprietary License",
    ],
    scripts=[
        (Path("scripts") / "my-game-list-manage.py").as_posix(),
        (Path("scripts") / "my-game-list-run-tests-with-pg.sh").as_posix(),
        (Path("scripts") / "my-game-list-run-tests.sh").as_posix(),
        (Path("scripts") / "colors.sh").as_posix(),
        (Path("scripts") / "my-game-list-build.py").as_posix(),
        (Path("scripts") / "wait-for-postgresql.py").as_posix(),
        (Path("scripts") / "python_colors.py").as_posix(),
    ],
)

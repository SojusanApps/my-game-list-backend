"""This module is used as a git hook to check if the version and changelog have been changed."""

import argparse
from collections.abc import Sequence

FILENAMES_TO_BE_MODIFIED = ("CHANGELOG.md", "my_game_list/__init__.py")


def main(argv: Sequence[str] | None = None) -> int:
    """Check if version and changelog are updated."""
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to check.")
    args = parser.parse_args(argv)

    return_value = 0
    for filename in FILENAMES_TO_BE_MODIFIED:
        if filename not in args.filenames:
            print(f"Missing required file: {filename}")  # noqa: T201
            return_value = 1
    return return_value


if __name__ == "__main__":
    raise SystemExit(main())

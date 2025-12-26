"""This package contains all the base functionalities used across all applications."""

from my_game_list.my_game_list.celery import app as celery_app

__all__ = ("celery_app",)

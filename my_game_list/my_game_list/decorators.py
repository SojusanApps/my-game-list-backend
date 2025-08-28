"""This module contains the decorators."""

import functools
from collections.abc import Callable, Mapping, Sequence
from typing import Any

import psutil

from my_game_list.my_game_list.metrics import Metrics


def calculate_cpu_usage_metric(func: Callable[[Any], Any]) -> Any:  # noqa: ANN401
    """Decorator responsible for calculating CPU usage and setting this value in the `cpu_usage_metric` metric."""

    @functools.wraps(func)
    def wrapper(*args: Sequence[Any], **kwargs: Mapping[str, Any]) -> Any:  # noqa: ANN401
        """This is just a wrapper function that sets the cpu usage."""
        Metrics.cpu_usage_metric.set(psutil.cpu_percent())
        return func(*args, **kwargs)

    return wrapper


def calculate_memory_usage_metric(func: Callable[[Any], Any]) -> Any:  # noqa: ANN401
    """Decorator responsible for calculating memory usage and setting this value in the `memory_usage_metric` metric."""

    @functools.wraps(func)
    def wrapper(*args: Sequence[Any], **kwargs: Mapping[str, Any]) -> Any:  # noqa: ANN401
        """This is just a wrapper function that sets the memory usage."""
        Metrics.memory_usage_metric.set(psutil.virtual_memory().percent)
        return func(*args, **kwargs)

    return wrapper

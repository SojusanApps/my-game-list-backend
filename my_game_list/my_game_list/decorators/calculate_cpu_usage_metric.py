"""This module contains the decorators."""

import functools
from collections.abc import Callable, Mapping, Sequence
from typing import Any

import psutil


def calculate_cpu_usage_metric(func: Callable[[Any], Any]) -> Any:  # noqa: ANN401
    """Decorator responsible for calculating CPU usage and setting this value in the `cpu_usage_metric` metric."""

    @functools.wraps(func)
    def wrapper(*args: Sequence[Any], **kwargs: Mapping[str, Any]) -> Any:  # noqa: ANN401
        """This is just a wrapper function that sets the cpu usage."""
        from my_game_list.my_game_list.metrics import Metrics

        Metrics.cpu_usage_metric.set(psutil.cpu_percent())
        return func(*args, **kwargs)

    return wrapper

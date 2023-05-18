import functools

import psutil


def calculate_memory_usage_metric(func):
    """Decorator responsible for calculating memory usage and setting this value in the `memory_usage_metric` metric."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        from my_game_list.my_game_list.metrics import Metrics

        Metrics.memory_usage_metric.set(psutil.virtual_memory().percent)
        return func(*args, **kwargs)

    return wrapper

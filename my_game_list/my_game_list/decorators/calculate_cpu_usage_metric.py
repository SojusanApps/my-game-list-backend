import functools

import psutil


def calculate_cpu_usage_metric(func):
    """Decorator responsible for calculating CPU usage and setting this value in the `cpu_usage_metric` metric."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        from my_game_list.my_game_list.metrics import Metrics

        Metrics.cpu_usage_metric.set(psutil.cpu_percent())
        return func(*args, **kwargs)

    return wrapper

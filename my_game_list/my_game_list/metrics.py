"""This module contains the custom Prometheus metrics."""

from prometheus_client import Gauge


class Metrics:
    """A class containing custom metrics."""

    cpu_usage_metric = Gauge("cpu_usage_percent", "CPU usage percentage.")
    memory_usage_metric = Gauge("memory_usage_percent", "Percentage of memory usage.")

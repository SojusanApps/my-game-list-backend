"""This module contains the custom Prometheus metrics."""

from django.http import HttpResponse
from django_prometheus.exports import ExportToDjangoView
from prometheus_client import Gauge
from rest_framework.request import Request

from my_game_list.my_game_list.decorators import calculate_cpu_usage_metric, calculate_memory_usage_metric


class Metrics:
    """A class containing custom metrics."""

    cpu_usage_metric = Gauge("cpu_usage_percent", "CPU usage percentage.")
    memory_usage_metric = Gauge("memory_usage_percent", "Percentage of memory usage.")


@calculate_memory_usage_metric
@calculate_cpu_usage_metric
def custom_export_to_django_view(request: Request) -> HttpResponse:
    """A wrapper for a function that returns metrics for Prometheus.

    Used to add decorators that configure custom values for metrics set during a request.
    """
    return ExportToDjangoView(request)

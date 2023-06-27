from django_prometheus.db.metrics import (
    connection_errors_total as connection_errors_total,
    connections_total as connections_total,
    errors_total as errors_total,
    execute_many_total as execute_many_total,
    execute_total as execute_total,
    query_duration_seconds as query_duration_seconds,
)
from prometheus_client import Counter as Counter

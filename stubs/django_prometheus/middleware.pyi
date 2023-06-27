from _typeshed import Incomplete
from django.utils.deprecation import MiddlewareMixin
from django_prometheus.conf import NAMESPACE as NAMESPACE, PROMETHEUS_LATENCY_BUCKETS as PROMETHEUS_LATENCY_BUCKETS
from django_prometheus.utils import PowersOf as PowersOf, Time as Time, TimeSince as TimeSince

class Metrics:
    @classmethod
    def get_instance(cls) -> Incomplete: ...
    def register_metric(
        self,
        metric_cls: Incomplete,
        name: Incomplete,
        documentation: Incomplete,
        labelnames: Incomplete = ...,
        **kwargs: Incomplete
    ) -> Incomplete: ...
    def __init__(self, *args: Incomplete, **kwargs: Incomplete) -> None: ...
    requests_total: Incomplete
    responses_total: Incomplete
    requests_latency_before: Incomplete
    requests_unknown_latency_before: Incomplete
    requests_latency_by_view_method: Incomplete
    requests_unknown_latency: Incomplete
    requests_ajax: Incomplete
    requests_by_method: Incomplete
    requests_by_transport: Incomplete
    requests_by_view_transport_method: Incomplete
    requests_body_bytes: Incomplete
    responses_by_templatename: Incomplete
    responses_by_status: Incomplete
    responses_by_status_view_method: Incomplete
    responses_body_bytes: Incomplete
    responses_by_charset: Incomplete
    responses_streaming: Incomplete
    exceptions_by_type: Incomplete
    exceptions_by_view: Incomplete
    def register(self) -> None: ...

class PrometheusBeforeMiddleware(MiddlewareMixin):
    metrics_cls = Metrics
    metrics: Incomplete
    def __init__(self, *args: Incomplete, **kwargs: Incomplete) -> None: ...
    def process_request(self, request: Incomplete) -> None: ...
    def process_response(self, request: Incomplete, response: Incomplete) -> Incomplete: ...

class PrometheusAfterMiddleware(MiddlewareMixin):
    metrics_cls = Metrics
    metrics: Incomplete
    def __init__(self, *args: Incomplete, **kwargs: Incomplete) -> None: ...
    def label_metric(
        self, metric: Incomplete, request: Incomplete, response: Incomplete | None = ..., **labels: Incomplete
    ) -> Incomplete: ...
    def process_request(self, request: Incomplete) -> None: ...
    def process_view(
        self, request: Incomplete, view_func: Incomplete, *view_args: Incomplete, **view_kwargs: Incomplete
    ) -> None: ...
    def process_template_response(self, request: Incomplete, response: Incomplete) -> Incomplete: ...
    def process_response(self, request: Incomplete, response: Incomplete) -> Incomplete: ...
    def process_exception(self, request: Incomplete, exception: Incomplete) -> None: ...

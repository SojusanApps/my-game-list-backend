from _typeshed import Incomplete

METRIC_EQUALS_ERR_EXPLANATION: str
METRIC_DIFF_ERR_EXPLANATION: str
METRIC_COMPARE_ERR_EXPLANATION: str
METRIC_DIFF_ERR_NONE_EXPLANATION: str

def assert_metric_equal(
    expected_value: Incomplete,
    metric_name: Incomplete,
    registry: Incomplete = ...,
    **labels: Incomplete,
) -> None: ...
def assert_metric_diff(
    frozen_registry: Incomplete,
    expected_diff: Incomplete,
    metric_name: Incomplete,
    registry: Incomplete = ...,
    **labels: Incomplete,
) -> None: ...
def assert_metric_no_diff(
    frozen_registry: Incomplete,
    expected_diff: Incomplete,
    metric_name: Incomplete,
    registry: Incomplete = ...,
    **labels: Incomplete,
) -> None: ...
def assert_metric_not_equal(
    expected_value: Incomplete,
    metric_name: Incomplete,
    registry: Incomplete = ...,
    **labels: Incomplete,
) -> None: ...
def assert_metric_compare(
    frozen_registry: Incomplete,
    predicate: Incomplete,
    metric_name: Incomplete,
    registry: Incomplete = ...,
    **labels: Incomplete,
) -> None: ...
def save_registry(registry: Incomplete = ...) -> Incomplete: ...
def get_metric(metric_name: Incomplete, registry: Incomplete = ..., **labels: Incomplete) -> Incomplete: ...
def get_metrics_vector(metric_name: Incomplete, registry: Incomplete = ...) -> Incomplete: ...
def get_metric_vector_from_frozen_registry(metric_name: Incomplete, frozen_registry: Incomplete) -> Incomplete: ...
def get_metric_from_frozen_registry(
    metric_name: Incomplete, frozen_registry: Incomplete, **labels: Incomplete
) -> Incomplete: ...
def format_labels(labels: Incomplete) -> Incomplete: ...
def format_vector(vector: Incomplete) -> Incomplete: ...

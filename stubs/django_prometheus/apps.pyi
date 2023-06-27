from _typeshed import Incomplete
from django.apps import AppConfig
from django_prometheus.exports import SetupPrometheusExportsFromConfig as SetupPrometheusExportsFromConfig
from django_prometheus.migrations import ExportMigrations as ExportMigrations

class DjangoPrometheusConfig(AppConfig):
    name: Incomplete
    verbose_name: str
    def ready(self) -> None: ...

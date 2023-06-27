"""This package contains all the settings configurations for the application."""
from django_stubs_ext import monkeypatch
from rest_framework.viewsets import GenericViewSet

monkeypatch(extra_classes=[GenericViewSet])

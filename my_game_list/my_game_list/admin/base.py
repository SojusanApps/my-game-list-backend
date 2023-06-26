"""This module contains the base model class for all admin dictionary models."""
from django.contrib import admin


class BaseDictionaryModelAdmin(admin.ModelAdmin):
    """Base admin model for dictionary."""

    readonly_fields = ("id",)
    search_fields = ("name",)
    list_display = (*readonly_fields, *search_fields)

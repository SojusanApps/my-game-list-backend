"""This module contains the base model class for all admin dictionary models."""
from django.contrib import admin

from my_game_list.my_game_list.models import BaseDictionaryModel


class BaseDictionaryModelAdmin(admin.ModelAdmin[BaseDictionaryModel]):
    """Base admin model for dictionary."""

    readonly_fields: tuple[str, ...] = ("id",)
    search_fields: tuple[str, ...] = ("name",)
    list_display: tuple[str, ...] = (*readonly_fields, *search_fields)

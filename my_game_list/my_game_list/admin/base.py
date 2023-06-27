"""This module contains the base model class for all admin dictionary models."""
from django.contrib import admin

from my_game_list.my_game_list.models import BaseDictionaryModel


class BaseDictionaryModelAdmin(admin.ModelAdmin[BaseDictionaryModel]):
    """Base admin model for dictionary."""

    readonly_fields = ("id",)
    search_fields = ("name",)
    list_display = (*readonly_fields, *search_fields)

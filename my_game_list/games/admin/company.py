"""This module contains the admin models for the Company."""

from django.contrib import admin

from my_game_list.games.models import Company
from my_game_list.my_game_list.admin import BaseDictionaryModelAdmin


@admin.register(Company)
class CompanyAdmin(BaseDictionaryModelAdmin):
    """Admin model for the company model."""

    readonly_fields = (*BaseDictionaryModelAdmin.readonly_fields, "company_logo_tag")
    list_display = (*BaseDictionaryModelAdmin.list_display, "company_logo_tag")

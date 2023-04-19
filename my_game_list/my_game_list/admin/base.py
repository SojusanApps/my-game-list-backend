from django.contrib import admin


class BaseDictionaryModelAdmin(admin.ModelAdmin):
    """Base admin model for dictionary."""

    readonly_fields = ("id",)
    search_fields = ("name",)
    list_display = readonly_fields + search_fields

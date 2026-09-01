from django.contrib import admin

from financial.models import ExceptionalCondition


@admin.register(ExceptionalCondition)
class ExceptionalConditionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "is_active", "rate_rule"
    )

    list_filter = ("rate_rule", "is_active")
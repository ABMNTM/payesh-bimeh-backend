from django.contrib import admin

from main.models import CostRateRule


@admin.register(CostRateRule)
class CostRateRuleAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "contract",
        "employment_type",
        "cost_type",
        "subsidy_percent",
        "base_premium_cost",
    )

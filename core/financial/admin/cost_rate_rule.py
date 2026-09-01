from django.contrib import admin

from financial.models import CostRateRule


@admin.register(CostRateRule)
class CostRateRuleAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "offer",
        "employment_type",
        "cost_type",
        "organ_share_percent",
        "base_premium_cost",
    )

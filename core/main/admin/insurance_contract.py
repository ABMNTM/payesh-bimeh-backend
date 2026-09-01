from django.contrib import admin

from main.models import InsuranceContract


@admin.register(InsuranceContract)
class InsuranceContractAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "contract_year",
        "insurer_company",
    )

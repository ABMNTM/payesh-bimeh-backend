from django.contrib import admin

from financial.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "enrollment", "success", "paid_at"
    )

    list_filter = ("enrollment", "enrollment__offer", "enrollment__offer__contract")

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from main.models import InsuranceOffer


@admin.register(InsuranceOffer)
class InsuranceOfferAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "contract__contract_year", "created_at"
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        queryset = InsuranceOffer.objects.select_related("contract")
        ordering = self.get_ordering(request)
        if ordering:
            queryset = queryset.order_by(*ordering)
        return queryset

    list_filter = ("contract",)

    search_fields = ("title",)

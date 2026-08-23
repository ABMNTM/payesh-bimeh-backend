from django.contrib import admin

from main.models import EmploymentType


@admin.register(EmploymentType)
class EmploymentTypeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "created_at",
    )

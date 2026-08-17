from django.contrib import admin

from main.models import Enrollment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):

    filter_horizontal = ("covered_members",)

    list_display = (
        "id",
        "status",
        "guardian",
        "contract",
        "terms_accepted_at",
    )

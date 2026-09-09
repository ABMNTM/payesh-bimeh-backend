from django.contrib import admin

from main.models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):

    search_fields = (
        "first_name",
        "last_name",
        "national_code",
        "personnel_code",
    )

    list_display = (
        "id",
        "first_name",
        "last_name",
        "national_code",
        "is_household_head",
    )

from django.contrib import admin

from main.models import SurveyAnschoice


@admin.register(SurveyAnschoice)
class SurveyAnschoiceAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "content",
        "created_at",
    )

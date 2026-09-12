from django.contrib import admin

from main.models import SurveyQuestion


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "content",
        "created_at",
    )
